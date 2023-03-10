# Stage 1: Install FFMPEG
FROM jrottenberg/ffmpeg:4.3-alpine AS ffmpeg

# Stage 2: Install application dependencies
FROM node:16-alpine

WORKDIR /app

COPY package.json .
COPY yarn.lock .

RUN yarn install --production

COPY . .

# Copy FFMPEG binaries from the first stage
COPY --from=ffmpeg /usr/local /usr/local

CMD ["npm", "start"]
