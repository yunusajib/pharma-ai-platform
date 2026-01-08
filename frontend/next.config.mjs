/** @type {import('next').NextConfig} */
import withPWA from '@ducanh2912/next-pwa';

const nextConfig = {
    reactStrictMode: true,
    // Force API URL for production
    env: {
        NEXT_PUBLIC_API_URL: 'https://pharma-ai-backend.onrender.com',
    },
};

export default withPWA({
    dest: 'public',
    register: true,
    skipWaiting: true,
    disable: process.env.NODE_ENV === 'development',
})(nextConfig);