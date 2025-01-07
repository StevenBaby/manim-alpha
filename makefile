
ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
$(eval $(ARGS):;@:)

%.h.mp4: src/%/main.py
	manim -p -qh -t -v INFO $< $(ARGS)

%.k.mp4: src/%/main.py
	manim -p -qk -t -v INFO $< $(ARGS)

%.mp4: src/%/main.py
	manim -p -ql -t -v INFO $< $(ARGS)

.PHONY: clean
clean:
	rm -rf media