# Define constants depending upon the microcontroller specifications

# How much memory can be allocated for the image only?
# Defined in bytes
# Set this to around 3/4 or any suitable fraction of the total RAM available
MAX_MEMORY_BUFFER_SIZE = 10000

# Current image being received
imagecount = 0

# Current serial byte being read
# Used for simulation of readSerialData()
# Is not required for actual program
serialcount = 0

# Arbitrary bytes to denote data and image
# Of course, in the actual code we only need to check for
#                                           JPEG start and end headers
DATA = 0x05
IMG = 0xff

# Flag variable to indicate if a new image is being read currently
imagestart = False

# Simulation of serial data
# Each image is received serially as IMG DATA DATA DATA DATA IMG i.e 6 bytes
# where IMG is a delimiter for a particular image
def readSerialData():
    global serialcount
    if(serialcount%5==0):
        return IMG
    else:
        return DATA

# Create an array of fixed memory for image, null indicates no image data there
NULL = 0x00
image_buffer = []
for i in xrange(0,MAX_MEMORY_BUFFER_SIZE):
    image_buffer.append(NULL)

# Basically this array is a queue, whenever it overflows we need to empty
# bytes into the file
queuestart = 0
queueend = 0
queuesize = MAX_MEMORY_BUFFER_SIZE
def writeToBuffer(byte):
    # Copy circular queue logic from any standard data structures book
    # Alternatively, consider using the collections.deque data structure
    # It implements a double-ended queue perfect for this application

    # Further, the only change required is that the byte must be written to file
    # if the queue overflows. Once written to file, you may free a byte from the
    # memory queue

    # In practice, overflow should be detected early on, rather than simply
    # giving a condition that occupied_size == MAX_MEMORY_BUFFER_SIZE.
    # This is because the incoming serial data may be too fast for you to keep
    # in the microcontroller's buffer before the memory queue is emptied.
    pass

# File pointer to current image being written
# Initially points to null
file = open(str(imagecount)+".txt","w")

# Replace imagecount<10 condition by any condition suitable for when the
# microcontroller should stop listening for serial bytes from camera
# This condition could involve checking if the flightstate is "LANDED",
# which means that no more images need to be taken.
while(imagecount<10):

    # readSerialData() is assumed to be a non-blocking call,
    # therefore the logic to parse the data from the other
    # sensors can be placed here.
    # In case there are bytes to read, we read them.
    if(readSerialData()==IMG):
        
        # If a new image is being read,
        # open a file pointer to a new image
        if(imagestart):
            file = open(str(imagecount)+".txt","w")
        else:
            file.close()
            
        # Invert the flag for imagestart, if it wasn't being read before
        # it is being read now and vice versa.
        imagestart ^= True

        # Write to buffer - IMG bytes
        # Actual code will check for start and end of JPEG header
        writeToBuffer(IMG)
    else:
        # Write to buffer - DATA bytes
        writeToBuffer(DATA)


