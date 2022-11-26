# In this file, I implement the fault injector for PySpark.
# Sam Williams, 2022


# Get args
while getopts :i:o: flag
do
    case "${flag}" in
        i) infilename=${OPTARG};;
	o) outfilename=${OPTARG};;
    esac
done

# Check args
if [ -z "$infilename" ] || [ -z "$outfilename" ]
then
  echo "Usage: '$0' -i <infilename> -o <outfilename>"
  exit 85
fi


# Check if the file exists
if [ ! -f "$infilename" ]; then
    echo "Error: the file '$infilename' does not exist."
    exit 1
fi


# Create updated injected file
echo "# PySpark Fault Injector by Sam Williams, 2022

import random
import struct

def _is_primitive(value):
    primitive = ((int, 'i'), (float, 'd'), (bool, '?'))
    return [(p,v) for (p,v) in primitive if isinstance(value, p)]

def SIMULATE_SDC(value, probability):
    # Condition for SDC occuring (changing value) based on probability
    primitive = _is_primitive(value)
    if random.random() <= probability and len(primitive) > 0:
        # 1. Get the original type and formatting code
        (t,code) = primitive[0]
        # 2. Convert to byte array
        bin_array = bytearray(struct.pack(code, value))
        # 3. Get the size
        sz = len(bin_array)
        # 4. Choose a bit to flip
        bit_to_flip = random.randrange(8*sz)
        # 5. Find that bit and flip it
        for i in range(sz):
            b = bin_array[i]
            if 8*(i+1) > bit_to_flip:
                # Fancy bit arithmetic
                bin_array[i] = b & ~(0b1 << (bit_to_flip % 8))
                # Convert it back to its type
                return struct.unpack(code, bin_array)[0]

    return value

" > "$outfilename"


# Read the rest of the input file
while IFS= read -r line; do
  printf '%s\n' "$line" >> "$outfilename"
done < "$infilename"
