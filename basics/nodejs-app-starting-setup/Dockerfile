FROM node

WORKDIR /app

COPY package.json package.json ./
COPY . /app

RUN npm install

EXPOSE 80

CMD ["node", "server.js"]