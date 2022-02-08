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
// File Name:  hgvs.go
//
// Author:  Jonathan Kans
//
// ==========================================================================

package eutils

import (
	"fmt"
	"os"
	"regexp"
	"sort"
	"strconv"
	"strings"
)

var (
	accnRegEx *regexp.Regexp
	genRegEx  *regexp.Regexp
	protRegEx *regexp.Regexp
)

// integer table for HGVS type used to define sort order
const (
	_ = iota
	GENOMIC
	CODING
	NONCODING
	MITOCONDRIAL
	RNA
	PROTEIN
)

var hgvsType = map[int]string{
	GENOMIC:      "Genomic",
	CODING:       "Coding",
	NONCODING:    "Noncoding",
	MITOCONDRIAL: "Mitochondrial",
	RNA:          "RNA",
	PROTEIN:      "Protein",
}

// integer table for HGVS class used to define sort order
const (
	_ = iota
	SUBS
	MIS
	TRM
	EXT
	SYN
	DEL
	INV
	DUP
	INS
	CONV
	INDEL
	FS
	TRANS
	REP
	MULT
)

var hgvsClass = map[int]string{
	SUBS:  "Substitution",
	MIS:   "Missense",
	TRM:   "Termination",
	EXT:   "Extension",
	SYN:   "Synonymous",
	DEL:   "Deletion",
	INV:   "Inversion",
	DUP:   "Duplication",
	INS:   "Insertion",
	CONV:  "Conversion",
	INDEL: "Indel",
	FS:    "Frameshift",
	TRANS: "Translocation",
	REP:   "Repetitive",
	MULT:  "Multiple",
}

// SPDI accession subfields used for controlling sort order
type SPDI struct {
	Type      int
	Class     int
	Accession string
	Prefix    string
	Number    int
	Version   int
	Position  int
	Deleted   string
	Inserted  string
}

var naConvert = map[string]string{
	"-": "-",
	"a": "A",
	"c": "C",
	"g": "G",
	"t": "T",
	"u": "T",
}

var aaConvert = map[string]string{
	"-":   "-",
	"*":   "*",
	"a":   "A",
	"b":   "B",
	"c":   "C",
	"d":   "D",
	"e":   "E",
	"f":   "F",
	"g":   "G",
	"h":   "H",
	"i":   "I",
	"j":   "J",
	"k":   "K",
	"l":   "L",
	"m":   "M",
	"n":   "N",
	"o":   "O",
	"p":   "P",
	"q":   "Q",
	"r":   "R",
	"s":   "S",
	"t":   "T",
	"u":   "U",
	"v":   "V",
	"w":   "W",
	"x":   "X",
	"y":   "Y",
	"z":   "Z",
	"ala": "A",
	"arg": "R",
	"asn": "N",
	"asp": "D",
	"asx": "B",
	"cys": "C",
	"gap": "-",
	"gln": "Q",
	"glu": "E",
	"glx": "Z",
	"gly": "G",
	"his": "H",
	"ile": "I",
	"leu": "L",
	"lys": "K",
	"met": "M",
	"phe": "F",
	"pro": "P",
	"pyl": "O",
	"sec": "U",
	"ser": "S",
	"stp": "*",
	"ter": "*",
	"thr": "T",
	"trp": "W",
	"tyr": "Y",
	"val": "V",
	"xle": "J",
	"xxx": "X",
}

// ParseHGVS parses sequence variant format into XML
func ParseHGVS(str string) string {

	// initialize variation description regular expressions
	if accnRegEx == nil {
		accnRegEx = regexp.MustCompile("\\*|\\d+|\\.|\\D+")
	}
	if genRegEx == nil {
		genRegEx = regexp.MustCompile("\\d+|\\D|>|\\D")
	}
	if protRegEx == nil {
		protRegEx = regexp.MustCompile("\\*|\\d+|\\D+")
	}

	// parse substitution
	parseSubs := func(typ, acc, vrn string) *SPDI {

		pos := ""
		ins := ""
		del := ""
		htype := 0
		class := 0
		ok := false

		// parse variation string
		switch typ {
		case "g":
			htype = GENOMIC

			arry := genRegEx.FindAllString(vrn, -1)
			if len(arry) != 4 {
				// fmt.Fprintf(os.Stderr, "\nERROR: Unrecognized variant '%s', array '%v'\n", vrn, arry)
				return nil
			}

			pos = arry[0]

			lf := strings.ToLower(arry[1])
			rt := strings.ToLower(arry[3])

			del, ok = naConvert[lf]
			if !ok {
				fmt.Fprintf(os.Stderr, "\nERROR: Unrecognized nucleotide '%s'\n", lf)
				return nil
			}
			ins, ok = naConvert[rt]
			if !ok {
				fmt.Fprintf(os.Stderr, "\nERROR: Unrecognized nucleotide '%s'\n", rt)
				return nil
			}

			class = SUBS
		case "p":
			htype = PROTEIN

			arry := protRegEx.FindAllString(vrn, -1)
			if len(arry) != 3 {
				// fmt.Fprintf(os.Stderr, "\nERROR: Unrecognized variant '%s', array '%v'\n", vrn, arry)
				return nil
			}

			pos = arry[1]

			lf := strings.ToLower(arry[0])
			rt := strings.ToLower(arry[2])

			del, ok = aaConvert[lf]
			if !ok {
				fmt.Fprintf(os.Stderr, "\nERROR: Unrecognized amino acid '%s'\n", lf)
				return nil
			}
			ins, ok = aaConvert[rt]
			if !ok {
				fmt.Fprintf(os.Stderr, "\nERROR: Unrecognized amino acid '%s'\n", rt)
				return nil
			}

			class = MIS
			if ins == "*" {
				class = TRM
			} else if del == "*" {
				class = EXT
			} else if del == ins {
				class = SYN
			}
		default:
			// fmt.Fprintf(os.Stderr, "\nWARNING: Parsing of HGVS type '%s' not yet implemented\n", typ)
			return nil
		}

		// position should be unsigned integer
		if !IsAllDigits(pos) {
			fmt.Fprintf(os.Stderr, "\nERROR: Non-integer position '%s'\n", pos)
			return nil
		}

		num, err := strconv.Atoi(pos)
		if err != nil {
			fmt.Fprintf(os.Stderr, "\nERROR: Integer conversion error '%s'\n", err)
			return nil
		}

		spdi := &SPDI{Type: htype, Class: class, Accession: acc, Position: num, Deleted: del, Inserted: ins}

		return spdi
	}

	// reality checks on variant type, will eventually call the different type-specific parsers
	parseOneType := func(typ, acc, vrn string) *SPDI {

		if strings.Index(vrn, "delins") >= 0 || strings.Index(vrn, "indel") >= 0 {
			// fmt.Fprintf(os.Stderr, "\nWARNING: deletion-insertion not yet implemented\n")
			return nil
		}
		if strings.Index(vrn, "del") >= 0 {
			// fmt.Fprintf(os.Stderr, "\nWARNING: deletion not yet implemented\n")
			return nil
		}
		if strings.Index(vrn, "inv") >= 0 {
			// fmt.Fprintf(os.Stderr, "\nWARNING: inversion not yet implemented\n")
			return nil
		}
		if strings.Index(vrn, "dup") >= 0 {
			// fmt.Fprintf(os.Stderr, "\nWARNING: duplication not yet implemented\n")
			return nil
		}
		if strings.Index(vrn, "con") >= 0 {
			// fmt.Fprintf(os.Stderr, "\nWARNING: conversion not yet implemented\n")
			return nil
		}
		if strings.Index(vrn, "ins") >= 0 {
			// fmt.Fprintf(os.Stderr, "\nWARNING: insertion not yet implemented\n")
			return nil
		}
		if strings.Index(vrn, "fs") >= 0 {
			// fmt.Fprintf(os.Stderr, "\nWARNING: frameshift not yet implemented\n")
			return nil
		}
		if strings.Index(vrn, "*") >= 0 {
			// fmt.Fprintf(os.Stderr, "\nWARNING: UTR variant not yet implemented\n")
			return nil
		}
		if strings.Index(vrn, "?") >= 0 {
			// fmt.Fprintf(os.Stderr, "\nWARNING: predictions not yet implemented\n")
			return nil
		}
		if strings.Index(vrn, ";") >= 0 {
			// fmt.Fprintf(os.Stderr, "\nWARNING: variation pairs not yet implemented\n")
			return nil
		}
		if strings.Index(vrn, "/") >= 0 {
			// fmt.Fprintf(os.Stderr, "\nWARNING: variation pairs not yet implemented\n")
			return nil
		}
		if strings.Index(vrn, "(") >= 0 || strings.Index(vrn, ")") >= 0 {
			// fmt.Fprintf(os.Stderr, "\nWARNING: intron variation not yet implemented\n")
			return nil
		}
		if strings.Index(vrn, "[") >= 0 || strings.Index(vrn, "]") >= 0 || strings.Index(vrn, ";") >= 0 {
			// fmt.Fprintf(os.Stderr, "\nWARNING: repetitive stretch not yet implemented\n")
			return nil
		}

		// otherwise use substitution
		return parseSubs(typ, acc, vrn)
	}

	var buffer strings.Builder

	var spdis []*SPDI

	ok := false

	// trim prefix and suffix
	str = strings.TrimPrefix(str, "HGVS=")
	idx := strings.Index(str, "|")
	if idx >= 0 {
		str = str[:idx]
	}

	// separate at commas
	htgs := strings.Split(str, ",")

	for _, htg := range htgs {

		// skip empty item
		if htg == "" {
			continue
		}

		// extract accession
		acc, rgt := SplitInTwoLeft(htg, ":")
		if acc == "" || rgt == "" {
			// fmt.Fprintf(os.Stderr, "\nERROR: Unable to parse HGVS '%s'\n", htg)
			continue
		}
		// split into type and variation
		typ, vrn := SplitInTwoLeft(rgt, ".")
		if typ == "" || vrn == "" {
			// fmt.Fprintf(os.Stderr, "\nERROR: Unable to parse HGVS '%s'\n", rgt)
			continue
		}

		// normalize variant string
		vrn = strings.TrimSpace(vrn)
		vrn = strings.ToLower(vrn)

		// predicted protein change enclosed in parentheses
		vrn = strings.TrimPrefix(vrn, "(")
		vrn = strings.TrimSuffix(vrn, ")")

		spdi := parseOneType(typ, acc, vrn)
		if spdi == nil {
			continue
		}

		// get accession fields for sorting
		pfx := ""
		num := ""
		ver := "0"

		// use regular expression to handle XX_ and XX_ABCD accessions
		arry := accnRegEx.FindAllString(acc, -1)
		if len(arry) == 2 {
			pfx = strings.ToUpper(arry[0])
			num = strings.ToLower(arry[1])
		} else if len(arry) == 4 {
			pfx = strings.ToUpper(arry[0])
			num = strings.ToLower(arry[1])
			ver = strings.ToLower(arry[3])
			if arry[2] != "." {
				fmt.Fprintf(os.Stderr, "\nERROR: Unable to parse version '%s', arry '%v'\n", acc, arry)
				continue
			}
		} else {
			fmt.Fprintf(os.Stderr, "\nERROR: Unable to parse accession '%s', arry '%v'\n", acc, arry)
			continue
		}

		if pfx == "" || num == "" {
			fmt.Fprintf(os.Stderr, "\nERROR: Unable to parse accession '%s'\n", acc)
			continue
		}

		// RefSeq accession body should be unsigned integer
		if !IsAllDigits(num) {
			fmt.Fprintf(os.Stderr, "\nERROR: Non-integer accession body '%s'\n", num)
			continue
		}

		val, err := strconv.Atoi(num)
		if err != nil {
			fmt.Fprintf(os.Stderr, "\nERROR: Integer conversion error '%s'\n", err)
			continue
		}

		vsn, err := strconv.Atoi(ver)
		if err != nil {
			fmt.Fprintf(os.Stderr, "\nERROR: Version error '%s'\n", err)
			continue
		}

		spdi.Prefix = pfx
		spdi.Number = val
		spdi.Version = vsn

		spdis = append(spdis, spdi)
		ok = true
	}

	if !ok {
		return ""
	}

	sort.Slice(spdis, func(i, j int) bool {
		a := spdis[i]
		b := spdis[j]
		if a.Type != b.Type {
			return a.Type < b.Type
		}
		if a.Class != b.Class {
			return a.Class < b.Class
		}
		if a.Prefix != b.Prefix {
			return a.Prefix < b.Prefix
		}
		// numeric comparison of accession digits ignores leading zeros
		if a.Number != b.Number {
			return a.Number < b.Number
		}
		// most recent version goes first
		if a.Version != b.Version {
			return a.Version > b.Version
		}
		if a.Position != b.Position {
			return a.Position < b.Position
		}
		if a.Deleted != b.Deleted {
			return a.Deleted < b.Deleted
		}
		if a.Inserted != b.Inserted {
			return a.Inserted < b.Inserted
		}
		return false
	})

	lastType := ""
	lastClss := ""

	for _, itm := range spdis {
		htyp := hgvsType[itm.Type]
		clss := hgvsClass[itm.Class]

		if lastClss != clss {
			if lastClss != "" {
				buffer.WriteString("</" + lastClss + ">\n")
			}
		}
		if lastType != htyp {
			if lastType != "" {
				buffer.WriteString("</" + lastType + ">\n")
			}
		}
		if lastType != htyp {
			lastType = htyp
			buffer.WriteString("<" + lastType + ">\n")
		}
		if lastClss != clss {
			lastClss = clss
			buffer.WriteString("<" + lastClss + ">\n")
		}

		pos := strconv.Itoa(itm.Position)
		buffer.WriteString("<Variant>" +
			"<Accession>" + itm.Accession + "</Accession>" +
			"<Position>" + pos + "</Position>" +
			"<Deleted>" + itm.Deleted + "</Deleted>" +
			"<Inserted>" + itm.Inserted + "</Inserted>" +
			"</Variant>\n")
	}

	if lastClss != "" {
		buffer.WriteString("</" + lastClss + ">\n")
	}
	if lastType != "" {
		buffer.WriteString("</" + lastType + ">\n")
	}

	return buffer.String()
}
