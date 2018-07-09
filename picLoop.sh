pwd

# activate venv
source myenv/bin/activate

# remove previously processed pics
for d in cropped_pic/*; do
	sudo find $d -iname "*invert*" -exec rm -i {} \;
	sudo find $d -iname "*output*" -exec rm -i {} \;

	# python colorManipulator.py -i $d
done

# process pics
for d in cropped_pic/*/*; do
	python src/colorManipulator.py -i $d
done
