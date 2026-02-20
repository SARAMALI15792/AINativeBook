import React from 'react';
import { NeuralNetworkBackground } from '@/components/effects/NeuralNetworkBackground';
import { Hero } from '@/components/landing/Hero';
import { FeatureCard } from '@/components/landing/FeatureCard';
import { TestimonialCarousel } from '@/components/landing/TestimonialCarousel';
import { Header } from '@/components/layout/Header';
import { Footer } from '@/components/layout/Footer';

export default function HomePage() {
  const features = [
    {
      icon: (
        <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
      ),
      title: 'AI-Powered Tutor',
      description: 'Get personalized guidance with our Socratic AI tutor that helps you learn by asking the right questions, not giving direct answers.',
    },
    {
      icon: (
        <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
        </svg>
      ),
      title: 'Interactive Simulations',
      description: 'Practice with Gazebo and NVIDIA Isaac Sim environments. Test your code in realistic robot simulations before deploying to hardware.',
    },
    {
      icon: (
        <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
        </svg>
      ),
      title: 'Structured Curriculum',
      description: '5-stage progressive learning path from ROS 2 fundamentals to advanced AI integration. Unlock stages as you master concepts.',
    },
    {
      icon: (
        <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
        </svg>
      ),
      title: 'Hands-On Projects',
      description: 'Build real robotics projects with step-by-step guidance. From autonomous navigation to object manipulation and human-robot interaction.',
    },
    {
      icon: (
        <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
      ),
      title: 'Community Learning',
      description: 'Join study groups, participate in forums, and connect with mentors. Learn together with a global community of robotics enthusiasts.',
    },
    {
      icon: (
        <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
        </svg>
      ),
      title: 'Earn Certificates',
      description: 'Complete stages and capstone projects to earn verified certificates. Showcase your robotics expertise to employers and institutions.',
    },
  ];

  const testimonials = [
    {
      id: '1',
      name: 'Sarah Chen',
      role: 'Robotics Engineer at Tesla',
      avatar: 'SC',
      content: 'IntelliStack transformed my career. The AI tutor helped me understand ROS 2 concepts deeply, and the hands-on projects gave me real-world experience.',
      rating: 5,
    },
    {
      id: '2',
      name: 'Marcus Johnson',
      role: 'PhD Student at MIT',
      avatar: 'MJ',
      content: 'The structured curriculum and interactive simulations made learning humanoid robotics accessible. I went from beginner to building my own autonomous systems.',
      rating: 5,
    },
    {
      id: '3',
      name: 'Priya Patel',
      role: 'Software Developer transitioning to Robotics',
      avatar: 'PP',
      content: 'As a career changer, I needed a platform that could meet me where I was. The personalized learning path and community support were game-changers.',
      rating: 5,
    },
  ];

  return (
    <main id="main-content" className="relative">
      {/* Navbar */}
      <Header transparent />

      {/* Neural Network Background */}
      <NeuralNetworkBackground />

      {/* Hero Section */}
      <Hero />

      {/* Features Section */}
      <section className="relative py-20 md:py-32">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16 space-y-4">
            <h2 className="text-4xl md:text-5xl font-bold text-text-primary">
              Everything You Need to Master Robotics
            </h2>
            <p className="text-xl text-text-secondary max-w-3xl mx-auto">
              From fundamentals to advanced AI integration, our platform provides comprehensive tools and resources for your robotics journey.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="animate-fade-in-up"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <FeatureCard
                  icon={feature.icon}
                  title={feature.title}
                  description={feature.description}
                />
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="relative py-20 md:py-32">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16 space-y-4">
            <h2 className="text-4xl md:text-5xl font-bold text-text-primary">
              Trusted by Learners Worldwide
            </h2>
            <p className="text-xl text-text-secondary max-w-3xl mx-auto">
              Join thousands of students, researchers, and professionals who have transformed their careers with IntelliStack.
            </p>
          </div>

          <div className="max-w-4xl mx-auto">
            <TestimonialCarousel
              testimonials={testimonials}
              autoRotate={true}
              rotateInterval={5000}
            />
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative py-20 md:py-32">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center space-y-8 glass backdrop-blur-md rounded-2xl p-12 md:p-16 border border-glass-border">
            <h2 className="text-4xl md:text-5xl font-bold text-text-primary">
              Ready to Start Your Robotics Journey?
            </h2>
            <p className="text-xl text-text-secondary">
              Join IntelliStack today and get access to AI-powered tutoring, interactive simulations, and a global community of learners.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
              <a
                href={`${process.env.NEXT_PUBLIC_DOCUSAURUS_URL || 'http://localhost:3002'}/stage-1/intro`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block px-8 py-4 bg-gradient-to-r from-accent-cyan to-accent-violet rounded-lg text-white font-semibold text-lg hover:shadow-glow-cyan transition-all duration-normal focus:outline-none focus:ring-2 focus:ring-accent-cyan"
              >
                Get Started Free
              </a>
              <a
                href={`${process.env.NEXT_PUBLIC_DOCUSAURUS_URL || 'http://localhost:3002'}/stage-1/intro`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block px-8 py-4 glass backdrop-blur-md rounded-lg text-text-primary font-semibold text-lg border border-accent-cyan hover:bg-glass-highlight transition-all duration-normal focus:outline-none focus:ring-2 focus:ring-accent-cyan"
              >
                Learn More
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <Footer />
    </main>
  );
}
