# image-duplicate-finder
Finds duplicate images in a very large database of images with least algorithmic complexity
Read image from disk -> Compute image Hash -> Search hash in a python dict -> Insert into the dict
In the search step an image is compared with all the images already encountered by the algorithm. The dict search happens in O(1) time. Doing this for all the n images gives O(n) complexity for the whole search.

idf-mt can do a full search and match of 2,00,000 images of CelebA dataset in 45 minutes on a 4 core 4GB laptop with HDD. HDD read was the main bottleneck happening at 5MB/s

## idf-st.py
Single threaded implementation of the image-duplicate-finder. Slow(in-efficient compute resource use) but easy to learn the algorithm. And of same compute complexity as idf-mt.py


##idf-mt.py
Multi-threaded implementation of the image-duplicate-finder. Parallelises read from the disk, and tries to hide disk access latency; which is very prominent in case of HDDs

Threads[n-1:0]
Read image from hardcoded location on the disk using n (n=8) threads
Compute the image hash using phash algorithm

Insert into mutithread safe queue

Thread n
Dequeue each hash from the queue and insert into a dict.
If already entry present at the hash, the new image is a duplicate of old image.


The whole algorithm is O(n) complexity; as the average complexity of search/insertion within dict is O(1)
