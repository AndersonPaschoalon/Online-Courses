# Etapa 1: build da aplicação (instalação de dependências)
FROM node:18 AS builder
WORKDIR /app
COPY src/package.json ./
RUN npm install
COPY src/ .

# Etapa 2: imagem final
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app .
EXPOSE 3000
CMD ["npm", "start"]



