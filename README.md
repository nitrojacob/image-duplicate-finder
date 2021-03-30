# image-duplicate-finder
Finds duplicate images in a very large database of images with least algorithmic complexity

Threads[15:0]
Read image from hardcoded location on the disk using n threads
Compute the image hash using phash algorithm

Insert into mutithread safe queue

Thread[16]
Dequeue each hash from the queue and insert into a dict.
If already entry present at the hash, the new image is a duplicate of old image.


The whole algorithm is O(n) complexity; as the average complexity of search/insertion within dict is O(1)
