// ===========================================================================
//
//                            PUBLIC DOMAIN NOTICE
//            National Center for Biotechnology Information (NCBI)
//
//  This software/database is a "United States Government Work" under the
//  terms of the United States Copyright Act. It was written as part of
//  the author's official duties as a United States Government employee and
//  thus cannot be copyrighted. This software/database is freely available
//  to the public for use. The National Library of Medicine and the U.S.
//  Government do not place any restriction on its use or reproduction.
//  We would, however, appreciate having the NCBI and the author cited in
//  any work or product based on this material.
//
//  Although all reasonable efforts have been taken to ensure the accuracy
//  and reliability of the software and data, the NLM and the U.S.
//  Government do not and cannot warrant the performance or results that
//  may be obtained by using this software or data. The NLM and the U.S.
//  Government disclaim all warranties, express or implied, including
//  warranties of performance, merchantability or fitness for any particular
//  purpose.
//
// ===========================================================================
//
// File Name:  align.go
//
// Author:  Jonathan Kans
//
// ==========================================================================

package eutils

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
	"unicode/utf8"
)

// AlignColumns aligns a tab-delimited table by individual column widths
func AlignColumns(inp io.Reader, margin, padding int, align string) <-chan string {

	if inp == nil {
		return nil
	}

	out := make(chan string, chanDepth)
	if out == nil {
		fmt.Fprintf(os.Stderr, "Unable to create alignment channel\n")
		os.Exit(1)
	}

	spcs := "                              "

	mrg := ""
	pad := "  "

	lettrs := make(map[int]rune)
	lst := 'l'

	if margin > 0 && margin < 30 {
		mrg = spcs[0:margin]
	}

	if padding > 0 && padding < 30 {
		pad = spcs[0:padding]
	}

	for i, ch := range align {
		lettrs[i] = ch
		lst = ch
	}

	alignTable := func(inp io.Reader, out chan<- string) {

		// close channel when all chunks have been sent
		defer close(out)

		var arry []string

		width := make(map[int]int)
		whole := make(map[int]int)
		fract := make(map[int]int)

		scanr := bufio.NewScanner(inp)

		row := 0
		numCols := 0

		// allows leading plus or minus, digits interspersed with optional commas, decimal point, and digits
		isNumeric := func(str string) bool {

			hasNum := false
			hasPeriod := false

			for i, ch := range str {
				switch ch {
				case '0', '1', '2', '3', '4', '5', '6', '7', '8', '9':
					hasNum = true
				case '+', '-':
					if i > 0 {
						return false
					}
				case '.':
					hasPeriod = true
				case ',':
					if hasPeriod {
						return false
					}
				default:
					return false
				}
			}

			return hasNum
		}

		processLine := func(line string) string {

			var flds []string

			cols := strings.Split(line, "\t")
			if numCols == 0 {
				numCols = len(cols)
			} else if numCols != len(cols) {
				fmt.Fprintf(os.Stderr, "ERROR: Mismatched number of columns in row ")
				fmt.Fprintf(os.Stderr, strconv.Itoa(row))
				fmt.Fprintf(os.Stderr, ": actual ")
				fmt.Fprintf(os.Stderr, strconv.Itoa(len(cols)))
				fmt.Fprintf(os.Stderr, ", expected ")
				fmt.Fprintf(os.Stderr, strconv.Itoa(numCols))
				fmt.Fprintf(os.Stderr, "\n")
				// os.Exit(1)
			}

			for i, str := range cols {

				str = CompressRunsOfSpaces(str)
				str = strings.TrimSpace(str)

				flds = append(flds, str)

				// determine maximum length in each column
				ln := utf8.RuneCountInString(str)
				if ln > width[i] {
					width[i] = ln
				}

				code, ok := lettrs[i]
				if !ok {
					code = lst
				}

				switch code {
				case 'n', 'N', 'z', 'Z':
					if isNumeric(str) {
						// determine maximum length of decimal number parts
						wh, fr := SplitInTwoLeft(str, ".")
						if fr != "" {
							fr = "." + fr
						}

						lf := utf8.RuneCountInString(wh)
						if lf > whole[i] {
							whole[i] = lf
						}
						rt := utf8.RuneCountInString(fr)
						if rt > fract[i] {
							fract[i] = rt
						}
						ln = whole[i] + fract[i]
						if ln > width[i] {
							width[i] = ln
						}
					}
				}
			}

			return strings.Join(flds, "\t")
		}

		for i := 0; i < numCols; i++ {

			code, ok := lettrs[i]
			if !ok {
				code = lst
			}

			switch code {
			case 'n', 'N', 'z', 'Z':
				// adjust maximum widths with aligned decimal points
				ln := whole[i] + fract[i]
				if ln > width[i] {
					width[i] = ln
				}
			}
		}

		// clean up spaces, calculate column widths
		for scanr.Scan() {

			row++
			line := scanr.Text()
			if line == "" {
				continue
			}

			line = processLine(line)
			arry = append(arry, line)
		}

		var buffer strings.Builder

		for _, line := range arry {

			buffer.Reset()

			cols := strings.Split(line, "\t")

			btwn := mrg
			for i, str := range cols {

				buffer.WriteString(btwn)

				code, ok := lettrs[i]
				if !ok {
					code = lst
				}

				ln := utf8.RuneCountInString(str)
				mx := width[i]
				diff := mx - ln
				lft := 0
				rgt := 0
				lftPad := " "
				rgtPad := " "

				if diff > 0 {
					switch code {
					case 'l':
						rgt = diff
					case 'c':
						lft = diff / 2
						rgt = diff - lft
					case 'r':
						lft = diff
					case 'n', 'N', 'z', 'Z':
						lft = diff
						if isNumeric(str) {
							switch code {
							case 'N':
								rgtPad = "0"
							case 'z':
								lftPad = "0"
							case 'Z':
								lftPad = "0"
								rgtPad = "0"
							}
							sn := whole[i]
							rc := fract[i]
							wh, fr := SplitInTwoLeft(str, ".")
							if fract[i] > 0 {
								if fr == "" {
									fr = "."
								} else {
									fr = "." + fr
								}
								lf := utf8.RuneCountInString(wh)
								lft = sn - lf
								rt := utf8.RuneCountInString(fr)
								rgt = rc - rt
								str = wh + fr
							}
						}
					default:
						rgt = diff
					}
				}

				for lft > 0 {
					lft--
					buffer.WriteString(lftPad)
				}

				buffer.WriteString(str)
				btwn = pad

				for rgt > 0 {
					rgt--
					buffer.WriteString(rgtPad)
				}
			}

			txt := buffer.String()
			txt = strings.TrimRight(txt, " ") + "\n"

			if txt != "" {
				out <- txt
			}
		}
	}

	// launch single alignment goroutine
	go alignTable(inp, out)

	return out
}
