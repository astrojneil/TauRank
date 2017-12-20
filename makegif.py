import imageio
images = []
filenames = []

pathToImages = raw_input('Path to Images: ')
ImageList = raw_input('Image List Name: ')

f = open(pathToImages+'/'+ImageList, 'r')
for line in f:
	filenames.append(str(line)[:-1])

gifName = pathToImages+'/'+ImageList[:-4]+'.gif'

for filename in filenames:
	name = pathToImages+'/'+filename
   	images.append(imageio.imread(name))
imageio.mimsave(gifName, images,duration=1.0)
