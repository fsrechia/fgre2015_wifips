from parsing import parsing_file
from func import get_alpha, get_estimate, get_distance
import sys

file_name = sys.argv[1]

out = parsing_file(file_name)
alpha = get_alpha(out)
get_estimate(out, alpha)
