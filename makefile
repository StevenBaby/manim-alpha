
%.h.mp4: src/%/main.py
	manim -p -qh -t -v INFO $< Video

%.k.mp4: src/%/main.py
	manim -p -qk -t -v INFO $< Video

%.mp4: src/%/main.py
	manim -p -ql -t -v INFO $< Video

.PHONY: clean
clean:
	rm -rf media