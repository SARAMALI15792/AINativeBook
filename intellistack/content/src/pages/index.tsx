import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/stage-1/intro">
            Start Learning →
          </Link>
        </div>
      </div>
    </header>
  );
}

function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          <div className="col col--4">
            <h3>Progressive Learning</h3>
            <p>
              Master robotics through 5 carefully structured stages, from fundamentals to advanced AI integration.
            </p>
          </div>
          <div className="col col--4">
            <h3>Simulation First</h3>
            <p>
              Learn with cloud-based Gazebo and Isaac Sim environments. No expensive hardware required to start.
            </p>
          </div>
          <div className="col col--4">
            <h3>AI-Powered Support</h3>
            <p>
              Get help from our Socratic AI tutor and RAG-powered chatbot. Learn by understanding, not just copying.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="AI-Native Learning Platform for Physical AI & Humanoid Robotics">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
