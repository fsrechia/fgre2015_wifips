from parsing import parsing_file
from rssi_func import centroid_weighted
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
	logger.info('Running main()')
	file_name = str(sys.argv[1])
	print file_name
	logger.info('File name is set to ' + file_name)

	logger.info('Print the output')
	output = parsing_file(file_name)
	centroid_weighted(output)

if __name__ == "__main__":
	main()
