FROM node:18-slim

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

COPY . .

CMD ["npm", "run", "serve"]
#CMD ["npm", "run", "build"]
