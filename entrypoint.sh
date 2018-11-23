#!/bin/sh

set -x

die() {
    echo $@ >&2
    exit -1
}

read_secret () {
    SECRETS_DIR=${SECRETS_DIR-/run/secrets}
    SECRETS_OUT_DIR=${SECRETS_OUT_DIR-/tmp/secrets}
    DECODER=${DECODER-base64 -d}
    mkdir -p $SECRETS_OUT_DIR || die "failed to create path $SECRETS_OUT_DIR"
    for sec in $(ls $SECRETS_DIR 2>/dev/null || echo "$SECRETS_DIR does not exist, running without secrets" >&2) ; do
        $DECODER $SECRETS_DIR/$sec > $SECRETS_OUT_DIR/$sec || die "Base 64 decoding failed on: $sec"
        echo "Exporting $sec"
        export $sec="$(cat $SECRETS_OUT_DIR/$sec)" || die "Cannot export content: $sec"
        echo "Exporting ${sec}_PATH"
        export ${sec}_PATH=$SECRETS_OUT_DIR/$sec || die "Cannot export path: $sec"
    done
}

read_secret

exec /gh-es.py "$@"
