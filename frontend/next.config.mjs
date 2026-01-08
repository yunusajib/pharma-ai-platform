/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  turbopack: {},
  env: {
    NEXT_PUBLIC_API_URL: 'https://pharma-ai-backend.onrender.com',
  },
};

export default nextConfig;
