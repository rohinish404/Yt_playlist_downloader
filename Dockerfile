                    # Dockerfile
FROM railwayapp/node:16

RUN apt-get update && \
    apt-get install -y ffmpeg

WORKDIR /app
COPY . .

CMD ["npm", "start"]
