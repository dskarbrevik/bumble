FREEROUTING_VERSION := 2.2.4
FREEROUTING_JAR := tools/freerouting-$(FREEROUTING_VERSION).jar
FREEROUTING_URL := https://github.com/freerouting/freerouting/releases/download/v$(FREEROUTING_VERSION)/freerouting-$(FREEROUTING_VERSION).jar

GREEN  := \033[0;32m
YELLOW := \033[1;33m
RED    := \033[0;31m
NC     := \033[0m

.PHONY: setup
setup:  ## Install/verify the toolchain (idempotent — skips what's already present)
	@ok()   { printf "$(GREEN)✓$(NC) %s\n" "$$1"; }; \
	warn()  { printf "$(YELLOW)⚠$(NC) %s\n" "$$1"; }; \
	fail()  { printf "$(RED)✗$(NC) %s\n" "$$1"; exit 1; }; \
	\
	if command -v uv >/dev/null 2>&1; then \
		ok "uv ($$(uv --version | head -1))"; \
	else \
		fail "uv not found — install: curl -LsSf https://astral.sh/uv/install.sh | sh"; \
	fi; \
	\
	if uv sync --quiet; then \
		ok "python env (build123d, trimesh, pyvista)"; \
	else \
		fail "uv sync failed"; \
	fi; \
	\
	if command -v kicad-cli >/dev/null 2>&1; then \
		ok "kicad-cli ($$(kicad-cli version 2>/dev/null))"; \
	elif [ -x "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli" ]; then \
		ok "kicad-cli (KiCad.app — add to PATH for scripts: /Applications/KiCad/KiCad.app/Contents/MacOS)"; \
	else \
		warn "KiCad not found — install 9+ from https://www.kicad.org/download/ (needed for DRC + gerbers)"; \
	fi; \
	\
	if java -version >/dev/null 2>&1; then \
		ok "java ($$(java -version 2>&1 | head -1))"; \
	else \
		warn "no working java runtime — needed to run FreeRouting (brew install --cask temurin)"; \
	fi; \
	\
	if [ -f "$(FREEROUTING_JAR)" ]; then \
		ok "freerouting jar (already at $(FREEROUTING_JAR))"; \
	else \
		mkdir -p tools; \
		if curl -fsSL -o "$(FREEROUTING_JAR)" "$(FREEROUTING_URL)"; then \
			ok "freerouting jar (downloaded to $(FREEROUTING_JAR))"; \
		else \
			rm -f "$(FREEROUTING_JAR)"; \
			warn "freerouting download failed — fetch manually: $(FREEROUTING_URL)"; \
		fi; \
	fi; \
	\
	if [ -f .env ]; then \
		ok ".env (already present)"; \
	else \
		cp .env.example .env; \
		warn ".env created from .env.example — fill in DigiKey credentials"; \
	fi; \
	\
	printf "\nsetup complete.\n"
