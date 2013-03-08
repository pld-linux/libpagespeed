#!/bin/sh
set -xe

export LC_ALL=C

# import options
# remove everything unless it's remove has been disabled with "0"
# "v8=0" means "do not remove v8"
eval "$@"

# removes dir, if the bcond is not turned off
# .gyp and .gypi is always preserved, and foo.h in that dir
strip_system_dirs() {
	local dir lib bcond
	for dir in "$@"; do
		lib=${dir##*/}
		bcond=$(eval echo \$$lib)
		[ "${bcond:-1}" = 0 ] && continue

		# skip already removed dirs
		test -d $dir || continue

		find $dir -depth -mindepth 1 '!' '(' -name '*.gyp' -o -name '*.gypi' -o -path $dir/$lib.h ')' -print -delete
	done
}

strip_system_dirs \
	third_party/zlib \
> REMOVED-system_dirs.txt

find -type d '!' -name '.' -print0 | sort -zr | xargs -0 rmdir --ignore-fail-on-non-empty > REMOVED-dirs.txt

# report what's in them
for a in REMOVED-*.txt; do
	cat $a
done
