#! /usr/bin/python3

import csv

fileName = 'test.csv'
baseName = 'qs'
extension = '.csv'
lines = 500000

def main():
    breakFile()

def breakFile():
    content = []
    rowCounter = 0
    batchCounter = 0
    with open(fileName, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            content.append(row)
            rowCounter += 1
            if rowCounter % lines == 0:
                with open(baseName + str(batchCounter) + extension, 'w') as fileToWrite:
                    for i in range(batchCounter * lines, rowCounter):
                        fileToWrite.write(','.join(content[i]) + '\n')
                print('Finished writing ' + baseName + str(batchCounter) + extension)
                batchCounter +=1
    with open(baseName + str(batchCounter) + extension, 'w') as fileToWrite:
        for i in range(batchCounter * lines, rowCounter):
            fileToWrite.write(','.join(content[i]) + '\n')
        print('Finished writing ' + baseName + str(batchCounter) + extension)


if __name__ == '__main__':
    main()
    print('Done!')
