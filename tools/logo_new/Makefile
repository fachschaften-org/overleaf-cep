resized/logo_%.png: Makefile logo.svg
	@w=$$(echo '$*' | cut -dx -f1); \
	h=$$(echo '$*' | cut -dx -f2); \
	magick \
		-background none \
		logo.svg \
		-resize "$${w}x$${h}" \
		-gravity center \
		-extent "$${w}x$${h}" \
		"$@"

resized/logo_%.svg: Makefile logo.svg
	@w=$$(echo '$*' | cut -dx -f1); \
	h=$$(echo '$*' | cut -dx -f2); \
	sed "s/<svg width=\"135px\" height=\"157px\"/<svg width=\"$${w}px\" height=\"$${h}px\"/g" logo.svg > $@

resized/logo_full_%.png: Makefile logo_full.svg
	@w=$$(echo '$*' | cut -dx -f1); \
	h=$$(echo '$*' | cut -dx -f2); \
	magick \
		-background none \
		logo.svg \
		-resize "$${w}x$${h}" \
		-gravity center \
		-extent "$${w}x$${h}" \
		"$@"

resized/logo_%.svg: Makefile logo_full.svg
	@w=$$(echo '$*' | cut -dx -f1); \
	h=$$(echo '$*' | cut -dx -f2); \
	sed "s/<svg width=\"542px\" height=\"157px\"/<svg width=\"$${w}px\" height=\"$${h}px\"/g" logo_full.svg > $@
