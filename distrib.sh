# display the distribution of all the addresses in the heavyusers.txt file

while read in; do 
	sh checkdistrib.sh "$in";
done < filteredheavyusers.txt

