### 1st Problem: words from server 1 to server 2
Solution inside commit 
```bash
docker compose up
docker ps
docker exec -it linux1 bash
curl -X POST http://auth_server:5001/login \
     -H "Content-Type: application/json" \
     -d '{"username": "Rares", "password": "Rares"}' 
curl -X POST http://auth_server:5001/run_words_pipeline \
     -H "Authorization: Bearer <TOKEN>"
exit
docker exec -it auth_server2 bash
cd results
cat longest_words.txt
exit
docker compose down
```

### Broken Server
Solution in the comments inside commit 216cb88
```bash
uv run uvicorn server:app --reload
```


### Bad Script

```bash
docker compose up
docker ps
docker exec -it <f319eb1a4342> bash
apt install procps
ps aux
kill <4492>
docker compose down
```