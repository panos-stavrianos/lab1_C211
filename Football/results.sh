#!/bin/bash
get_index() {
  local value=$1
  shift
  local arr=("$@")
  local i=0
  for i in "${!arr[@]}"; do
    if [[ "${arr[$i]}" == "${value}" ]]; then
      echo "$i"
      return
    fi
  done
}

declare -a teams
declare -a points
declare -a goals_scored
declare -a goals_taken

add_to_tables() {
  local team=$1
  local score1=$2
  local score2=$3
  local index=0
  local new_index=${#teams[@]}               # array current length
  index="$(get_index "$team" "${teams[@]}")" # get the index of the team if exists on the array

  if [ -z "$index" ]; then # if not exists, init with empty values
    teams+=("")
    points+=(0)
    goals_scored+=(0)
    goals_taken+=(0)
    index=$new_index
  fi

  teams[$index]="$team" # team name
  if ((score1 > score2)); then # team won
    points[$index]=$((points[index] + 3)) # adding 3 points
  elif ((score1 < score2)); then # team lost
    points[$index]=$((points[index] + 0)) # adding 0 points -obviously unnecessary-
  else # draw
    points[$index]=$((points[index] + 1)) # adding 1 point
  fi
  goals_scored[$index]=$((goals_scored[index] + score1))
  goals_taken[$index]=$((goals_taken[index] + score2))

}
# read line by line the file
for line in $(<"$1"); do
  # Ομάδα1-Ομάδα2:Σκορ1-Σκορ2
  IFS=':' read -r -a a1 <<<"$line"                              # spliting with :
  IFS='-' read -r -a two_teams <<<"${a1[0]}"                    # spliting with - the teams
  IFS='-' read -r -a scores <<<"${a1[1]}"                       # spliting with - the scores
  add_to_tables "${two_teams[0]}" "${scores[0]}" "${scores[1]}" # team1 name, team 1 goals scored, team 1 goals taken
  add_to_tables "${two_teams[1]}" "${scores[1]}" "${scores[0]}" # team2 name, team 2 goals scored, team 2 goals taken
done

format() {
  for i in "${!teams[@]}"; do
    echo -e "${teams[$i]}\t${points[$i]}\t${goals_scored[$i]}-${goals_taken[$i]}"
  done
}

sorted=$("format" | sort -t$'\t' -k2r,2n -k1,1)
final=$(echo -e "$sorted" | awk '{print NR  ".\t" $s}')
#
echo -e "$final" | column -t
