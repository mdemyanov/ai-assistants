#!/usr/bin/env bash
# AI Skills Installer
# Установка skills для Claude Desktop
#
# Использование:
#   curl -sSL https://raw.githubusercontent.com/USER/ai-assistants/main/scripts/install.sh | bash
#   curl -sSL ... | bash -s -- --skill prompt-creator
#   curl -sSL ... | bash -s -- --list

set -euo pipefail

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Конфигурация
REPO="mdemyanov/ai-assistants"
API_URL="https://api.github.com/repos/${REPO}/releases/latest"

# Определение директории skills
detect_skills_dir() {
    case "$(uname -s)" in
        Darwin)
            echo "$HOME/Library/Application Support/Claude/skills"
            ;;
        Linux)
            # Проверяем WSL
            if grep -qi microsoft /proc/version 2>/dev/null; then
                # WSL: используем Windows путь
                APPDATA=$(cmd.exe /c "echo %APPDATA%" 2>/dev/null | tr -d '\r')
                echo "${APPDATA}/Claude/skills"
            else
                echo "$HOME/.config/claude/skills"
            fi
            ;;
        *)
            echo "$HOME/.claude/skills"
            ;;
    esac
}

SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$(detect_skills_dir)}"

# Функции
print_header() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════╗"
    echo "║     AI Skills Installer              ║"
    echo "╚══════════════════════════════════════╝"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1" >&2
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Проверка зависимостей
check_dependencies() {
    local missing=()

    command -v curl >/dev/null 2>&1 || missing+=("curl")
    command -v unzip >/dev/null 2>&1 || missing+=("unzip")
    command -v jq >/dev/null 2>&1 || missing+=("jq")

    if [ ${#missing[@]} -ne 0 ]; then
        print_error "Missing dependencies: ${missing[*]}"
        echo "Install them with:"
        case "$(uname -s)" in
            Darwin)
                echo "  brew install ${missing[*]}"
                ;;
            Linux)
                echo "  sudo apt-get install ${missing[*]}"
                ;;
        esac
        exit 1
    fi
}

# Получить информацию о последнем релизе
get_latest_release() {
    curl -s "$API_URL"
}

# Список доступных skills
list_skills() {
    print_header
    print_info "Fetching available skills..."

    local release
    release=$(get_latest_release)

    local version
    version=$(echo "$release" | jq -r '.tag_name')

    echo ""
    echo "Latest release: ${version}"
    echo ""
    echo "Available skills:"
    echo ""

    echo "$release" | jq -r '.assets[].name' | while read -r asset; do
        # Убираем расширение .zip и версию
        local skill_name
        skill_name=$(echo "$asset" | sed 's/_v[0-9.]*\.zip$//' | sed 's/\.zip$//')
        echo "  - ${skill_name}"
    done

    echo ""
    print_info "Install all: curl -sSL ... | bash"
    print_info "Install one: curl -sSL ... | bash -s -- --skill <name>"
}

# Установка skill
install_skill() {
    local url=$1
    local filename=$2

    print_info "Downloading ${filename}..."

    local tmp_file="/tmp/${filename}"
    curl -sL "$url" -o "$tmp_file"

    print_info "Extracting to ${SKILLS_DIR}..."
    unzip -o "$tmp_file" -d "$SKILLS_DIR" >/dev/null

    rm -f "$tmp_file"
    print_success "Installed ${filename}"
}

# Установка всех skills
install_all() {
    print_header

    print_info "Fetching latest release..."
    local release
    release=$(get_latest_release)

    local version
    version=$(echo "$release" | jq -r '.tag_name')
    print_success "Found release ${version}"

    # Создаём директорию
    mkdir -p "$SKILLS_DIR"
    print_info "Installing to: ${SKILLS_DIR}"
    echo ""

    # Скачиваем и устанавливаем каждый asset
    echo "$release" | jq -r '.assets[] | "\(.browser_download_url) \(.name)"' | while read -r url filename; do
        install_skill "$url" "$filename"
    done

    echo ""
    print_success "Installation complete!"
    echo ""
    print_info "Restart Claude Desktop to activate skills"
}

# Установка конкретного skill
install_one() {
    local skill_name=$1

    print_header
    print_info "Fetching latest release..."

    local release
    release=$(get_latest_release)

    local version
    version=$(echo "$release" | jq -r '.tag_name')

    # Ищем asset по имени
    local asset
    asset=$(echo "$release" | jq -r ".assets[] | select(.name | startswith(\"${skill_name}\"))")

    if [ -z "$asset" ]; then
        print_error "Skill '${skill_name}' not found in release ${version}"
        echo ""
        echo "Available skills:"
        echo "$release" | jq -r '.assets[].name' | sed 's/_v[0-9.]*\.zip$//' | sed 's/\.zip$//' | while read -r name; do
            echo "  - ${name}"
        done
        exit 1
    fi

    local url
    url=$(echo "$asset" | jq -r '.browser_download_url')
    local filename
    filename=$(echo "$asset" | jq -r '.name')

    # Создаём директорию
    mkdir -p "$SKILLS_DIR"

    install_skill "$url" "$filename"

    echo ""
    print_success "Installation complete!"
    print_info "Restart Claude Desktop to activate the skill"
}

# Обновление всех skills
update_all() {
    print_info "Updating all skills..."
    install_all
}

# Удаление skill
uninstall_skill() {
    local skill_name=$1

    local skill_path="${SKILLS_DIR}/${skill_name}"

    if [ ! -d "$skill_path" ]; then
        print_error "Skill '${skill_name}' not found at ${skill_path}"
        exit 1
    fi

    rm -rf "$skill_path"
    print_success "Uninstalled ${skill_name}"
}

# Парсинг аргументов
main() {
    local action="install_all"
    local skill_name=""

    while [[ $# -gt 0 ]]; do
        case $1 in
            --list|-l)
                action="list"
                shift
                ;;
            --skill|-s)
                action="install_one"
                skill_name="$2"
                shift 2
                ;;
            --update|-u)
                action="update"
                shift
                ;;
            --uninstall)
                action="uninstall"
                skill_name="$2"
                shift 2
                ;;
            --help|-h)
                echo "Usage: install.sh [OPTIONS]"
                echo ""
                echo "Options:"
                echo "  --list, -l          List available skills"
                echo "  --skill, -s NAME    Install specific skill"
                echo "  --update, -u        Update all installed skills"
                echo "  --uninstall NAME    Uninstall a skill"
                echo "  --help, -h          Show this help"
                echo ""
                echo "Environment:"
                echo "  CLAUDE_SKILLS_DIR   Custom skills directory"
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done

    check_dependencies

    case $action in
        list)
            list_skills
            ;;
        install_all)
            install_all
            ;;
        install_one)
            install_one "$skill_name"
            ;;
        update)
            update_all
            ;;
        uninstall)
            uninstall_skill "$skill_name"
            ;;
    esac
}

main "$@"
