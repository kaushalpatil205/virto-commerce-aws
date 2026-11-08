#!/bin/bash
set -e

echo "=========================================================="
echo "Setting up Virto Commerce Modern B2B Headless Frontend"
echo "=========================================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$ROOT_DIR"

# 1. Official Modern B2B Vue 3 Theme
echo -e "\n[1/5] Downloading Official Modern B2B Theme (vc-frontend v2.61.0)..."
mkdir -p cms-content/Themes/B2B-store/default
curl -s -L -o /tmp/vc-theme-b2b-vue.zip "https://github.com/VirtoCommerce/vc-frontend/releases/download/2.61.0/vc-theme-b2b-vue-2.61.0.zip"
unzip -q -o /tmp/vc-theme-b2b-vue.zip -d cms-content/Themes/B2B-store/default/
rm -f /tmp/vc-theme-b2b-vue.zip
echo "  ✓ Modern B2B Theme installed into cms-content/Themes/B2B-store/default"

# 2. XFrontend Module
echo -e "\n[2/5] Downloading VirtoCommerce.XFrontend (v3.1009.0)..."
mkdir -p modules/VirtoCommerce.XFrontend
curl -s -L -o /tmp/xfrontend.zip "https://github.com/VirtoCommerce/vc-module-x-frontend/releases/download/3.1009.0/VirtoCommerce.XFrontend_3.1009.0.zip"
unzip -q -o /tmp/xfrontend.zip -d modules/VirtoCommerce.XFrontend/
rm -f /tmp/xfrontend.zip
echo "  ✓ VirtoCommerce.XFrontend installed"

# 3. WhiteLabeling Module
echo -e "\n[3/5] Downloading VirtoCommerce.WhiteLabeling (v3.1006.0)..."
mkdir -p modules/VirtoCommerce.WhiteLabeling
curl -s -L -o /tmp/whitelabeling.zip "https://github.com/VirtoCommerce/vc-module-white-labeling/releases/download/3.1006.0/VirtoCommerce.WhiteLabeling_3.1006.0.zip"
unzip -q -o /tmp/whitelabeling.zip -d modules/VirtoCommerce.WhiteLabeling/
rm -f /tmp/whitelabeling.zip
echo "  ✓ VirtoCommerce.WhiteLabeling installed"

# 4. ImageTools Module
echo -e "\n[4/5] Downloading VirtoCommerce.ImageTools (v3.1009.0)..."
mkdir -p modules/VirtoCommerce.ImageTools
curl -s -L -o /tmp/imagetools.zip "https://github.com/VirtoCommerce/vc-module-image-tools/releases/download/3.1009.0/VirtoCommerce.ImageTools_3.1009.0.zip"
unzip -q -o /tmp/imagetools.zip -d modules/VirtoCommerce.ImageTools/
rm -f /tmp/imagetools.zip
echo "  ✓ VirtoCommerce.ImageTools installed"

# 5. ProfileExperienceApi Module
echo -e "\n[5/5] Downloading VirtoCommerce.ProfileExperienceApiModule (v3.1023.0)..."
mkdir -p modules/VirtoCommerce.ProfileExperienceApiModule
curl -s -L -o /tmp/profile.zip "https://github.com/VirtoCommerce/vc-module-profile-experience-api/releases/download/3.1023.0/VirtoCommerce.ProfileExperienceApiModule_3.1023.0.zip"
unzip -q -o /tmp/profile.zip -d modules/VirtoCommerce.ProfileExperienceApiModule/
rm -f /tmp/profile.zip
echo "  ✓ VirtoCommerce.ProfileExperienceApiModule installed"

echo -e "\n=========================================================="
echo "Modern Frontend & Experience Modules successfully setup!"
echo "=========================================================="
