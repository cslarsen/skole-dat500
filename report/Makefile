OS := $(shell uname)

ifeq ($(OS),Linux)
	PDFLATEX := /opt-rh7/texlive/2017/bin/x86_64-linux/pdflatex
	BIBTEX := /opt-rh7/texlive/2017/bin/x86_64-linux/bibtex
	OPEN := xdg-open
	DETEX := /opt-rh7/texlive/2017/bin/x86_64-linux/detex 
else
	PDFLATEX := pdflatex
	BIBTEX := bibtex
	OPEN := open
	DETEX := detex
endif

TARGETS := \
	assignment-1.pdf \
	assignment-2.pdf

CURRENT := dat510-assignment-2.pdf

all: $(TARGETS)

freqs.pdf: freqs.R
	Rscript $< && mv Rplots.pdf $@

check:
	$(DETEX) $(CURRENT:.pdf=.text) | diction -bs

open: $(CURRENT)
	$(OPEN) $(CURRENT)

%.eps: %.gp data.txt
	gnuplot $<

assignment-1.pdf: freqs.pdf

%.pdf: %.tex %.bib preamble.tex
	$(PDFLATEX) -halt-on-error $<
	$(BIBTEX) $(<:.tex=)
	$(PDFLATEX) -halt-on-error $<
	$(PDFLATEX) -halt-on-error $<

clean:
	rm -f $(TARGETS) $(TARGETS:.pdf=.aux) $(TARGETS:.pdf=.log) $(TARGETS:.pdf=.out)
