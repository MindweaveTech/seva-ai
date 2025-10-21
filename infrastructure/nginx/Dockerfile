FROM nginx:1.25-alpine

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Remove default config
RUN rm -f /etc/nginx/conf.d/default.conf

# Copy static HTML files
RUN mkdir -p /etc/nginx/html
COPY expo-connect.html /etc/nginx/html/expo-connect.html

# Create log directory
RUN mkdir -p /var/log/nginx

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/health || exit 1

CMD ["nginx", "-g", "daemon off;"]
