FROM node:lts-alpine as build-step
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package.json  ./
COPY ./src ./src
COPY ./public ./public
RUN npm install
RUN npm run build

# Build step #2: build an Caddy container
FROM caddy:alpine
EXPOSE 4000
COPY --from=build-step /app/build /usr/share/caddy