#!/usr/bin/env bash

cp -f img/*.png ../../services/web/public/
cp -f img/*.svg ../../services/web/public/
cp -f img/*.ico ../../services/web/public/

cp -f img/ol-brand/*.png ../../services/web/public/img/ol-brand/
cp -f img/ol-brand/*.svg ../../services/web/public/img/ol-brand/

# Explicitly include the dark Mallard variant
cp -f img/ol-brand/overleaf-a-ds-solution-mallard-dark.svg ../../services/web/public/img/ol-brand/ 

cp -f img/ol-brand/overleaf.svg ../../services/web/frontend/js/shared/svgs
cp -f img/ol-brand/overleaf-*.svg ../../services/web/frontend/js/shared/svgs

# Explicitly copy the dark Mallard variant into shared svgs as well
cp -f img/ol-brand/overleaf-a-ds-solution-mallard-dark.svg ../../services/web/frontend/js/shared/svgs 

