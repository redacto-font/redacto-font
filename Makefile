PYTHON ?= python3
SRC     = sources/build.py
FONTS   = fonts/Redacto-Regular.ttf fonts/Redacto-Regular.otf fonts/Redacto-Regular.woff2

.PHONY: all clean

all: $(FONTS)

$(FONTS): $(SRC)
	$(PYTHON) $(SRC)

clean:
	rm -f fonts/*.ttf fonts/*.otf fonts/*.woff2
