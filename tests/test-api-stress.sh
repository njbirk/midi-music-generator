for i in {1..50}; do 
  curl -X POST http://localhost:5000/get-song-file/
done
