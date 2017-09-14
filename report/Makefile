OS := $(shell uname)
MAIN := bachelor

ifeq ($(OS),Linux)
	PDFLATEX := /opt-rh7/texlive/2017/bin/x86_64-linux/pdflatex
	BIBTEX := /opt-rh7/texlive/2017/bin/x86_64-linux/bibtex
	OPEN := xdg-open
else
	PDFLATEX := pdflatex
	BIBTEX := bibtex
	OPEN := open
endif

TARGETS := dat510-assignment-1.pdf

all: $(TARGETS)

open: all
	$(OPEN) dat510-assignment-1.pdf

%.eps: %.gp data.txt
	gnuplot $<

dat510-assignment-1.pdf: dat510-assignment-1.tex preamble.tex

%.pdf: %.tex
	$(PDFLATEX) -halt-on-error dat510-assignment-1.tex
	$(BIBTEX) dat510-assignment-1 # NOTE: No extension
	$(PDFLATEX) -halt-on-error dat510-assignment-1.tex
	$(PDFLATEX) -halt-on-error dat510-assignment-1.tex

clean:
	rm -f $(TARGETS) $(TARGETS:.pdf=.aux) $(TARGETS:.pdf=.log) $(TARGETS:.pdf=.out)
