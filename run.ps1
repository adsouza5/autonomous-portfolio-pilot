# Build a fresh image (picks up any portfolio.json changes)
docker build -t robo-advisor-mvp .

# Run the container, loading your .env and mounting the local folder
docker run --rm `
  --env-file .env `
  -v "${PWD}:/app" `
  -w /app `
  robo-advisor-mvp
