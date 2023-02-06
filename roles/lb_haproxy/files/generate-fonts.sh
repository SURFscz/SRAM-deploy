#!/bin/bash

# this scripts takes an full web font (otf) and generates a smalller version with a minimal subset of glyphs
# useful for embedding etc

set -e

TMPFILE=$(mktemp 'fontsubset_XXXXXX')
cat > $TMPFILE <<EOF
    A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,T,S,U,V,W,X,Y,Z
    a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,t,s,u,v,w,x,y,z
    zero,one,two,three,four,five,six,seven,eight,nine
    comma,period,hyphen
    question,exclam
    at,ampersand
    space
EOF

for font in SourceSansPro-Regular SourceSansPro-Semibold
do
	echo ${font}
	fonttools subset \
		--recommended-glyphs --glyphs-file=$TMPFILE \
		--desubroutinize --flavor=woff2 \
		--output-file=${font}.subset.otf \
		${font}.otf
	base64 --wrap=0 < ${font}.subset.otf > ${font}.subset.otf.base64
done

rm $TMPFILE
exit 0
