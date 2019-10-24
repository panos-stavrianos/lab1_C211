#!/bin/bash
for file in "$@"; do

  declare -a X
  declare -a Y

  for line in $(<"$file"); do
    IFS=':' read -r -a a1 <<<"$line" # spliting with :
    X+=(${a1[0]})
    Y+=(${a1[1]})
  done

  length=${#X[@]}

  ## SUM_X
  sum_x=$(
    IFS="+"
    bc <<<"${X[*]}"
  )

  ## SUM_Y
  sum_y=$(
    IFS="+"
    bc <<<"${Y[*]}"
  )

  ## SUM_X2
  declare -a x2
  for ((i = 0; i < $length; i++)); do
    x2[i]="$(echo "scale=20; ${X[i]}*${X[i]}" | bc)"
  done

  sum_x2=$(
    IFS="+"
    bc <<<"${x2[*]}"
  )

  ## SUM_XY
  declare -a xy
  for ((i = 0; i < $length; i++)); do
    xy[i]="$(echo "scale=20; ${X[i]}*${Y[i]}" | bc)"
  done

  sum_xy=$(
    IFS="+"
    bc <<<"${xy[*]}"
  )

  ## a
  a_d=$(LC_NUMERIC=C printf %0.2f "$(echo "scale=20;  $length * $sum_x2 - $sum_x ^ 2" | bc)")
  if [ 1 -eq "$(echo "${a_d} == 0.00" | bc)" ]; then
    a=0
    c=1
  else
    a=$(LC_NUMERIC=C printf %0.2f "$(echo "scale=20;  ($length * $sum_xy - $sum_x * $sum_y) / $a_d" | bc)")
    c=0
  fi

  ## b
  b=$(LC_NUMERIC=C printf %0.2f "$(echo "scale=20;  ($sum_y - $a * $sum_x) / $length" | bc)")

  ## Error
  declare -a err
  for ((i = 0; i < $length; i++)); do
    err[i]="$(echo "scale=20; (${Y[i]} - ($a * ${X[i]} + $b)) ^ 2" | bc)"
  done

  error=$(
    IFS="+"
    bc <<<"${err[*]}"
  )
  error=$(LC_NUMERIC=C printf %0.2f "$error")

  #FILE: input2, a=-2.13 b=1.23 c=1 err=13.25
  echo "FILE: $file, a=$a b=$b c=$c err=$error"

  unset X
  unset Y
  unset x2
  unset xy
  unset err
done
