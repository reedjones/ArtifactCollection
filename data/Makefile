#
# This Makefile assumes you have a link to gist 4090846 in ./d
# (4090846 has files with US state names et al.)
# I did also set ./git/info/exclude with
# d/
# in order to ignore d/ for GIT
all: help

.PHONY : help
help:
	@echo "make us-state-names-plus.tsv .  generate US states' names"
	@echo "make us-state-flag-urls.tsv . . generate US state flags' URLs"
	@echo "make download-flags . . . . . . download SVG flags from Wikipedia Commons in 'flags' directory."
	@echo "make clean  . . . . . . . . . . remove all generated/downloaded files"


us-state-names-plus.tsv: us-state-names.tsv
	@head -n 52 $< | grep -v "Columbia" > $@
	@echo "11	DC	Washington, D.C." >> $@


us-state-flag-urls.tsv: us-state-names-plus.tsv
	for s in $$(cat $< | tail -n+2 | cut -f3 | sed -e 's/[ ][ ]*/_/g') ; do \
		h=$$(md5 -qs "Flag_of_$$s.svg" | cut -c1-2); \
		f=$$(echo $$h | cut -c1); \
                n=$$(echo $$s | sed -e 's/,/%2C/g'); \
		echo "http://upload.wikimedia.org/wikipedia/commons/$$f/$$h/Flag_of_$$n.svg"; \
	done > $@

us-state-ids.tsv: us-state-names-plus.tsv
	for i in $$(cat $< | tail -n+2 | cut -f1); do \
		echo $$(printf %02d $$i) ;\
	done > $@

us-state-id-flag-urls.tsv: us-state-ids.tsv us-state-flag-urls.tsv
	paste -d '|' $^ | while IFS='|' read -r i n; do \
	echo "$$i	$$n"; done > $@
	echo "id	url\n$$(cat $@)" > $@


.PHONY : download-flags
download-flags: us-state-id-flag-urls.tsv
	@mkdir -p flags
	@for u in $$(cat $< | tail -n+2 | cut -f 2) ; do \
		curl -s "$$u" > flags/$$(echo $$u | rev | cut -d'/' -f1 | rev | sed -e 's/%2C/,/g') ; \
	done



.PHONY : clean
clean:
	@rm -fr flags us-state-names-plus.tsv us-state-flag-urls.tsv us-state-id-flag-urls.tsv: us-state-ids.tsv
