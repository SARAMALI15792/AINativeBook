import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import path from 'path';

const config: Config = {
  title: 'IntelliStack',
  tagline: 'AI-Native Learning Platform for Physical AI & Humanoid Robotics',
  favicon: 'img/favicon.ico',

  // Local development configuration
  url: 'http://localhost:3002',
  baseUrl: '/',

  onBrokenLinks: 'ignore',
  markdown: {
    format: 'mdx',
    mermaid: true,
  },

  // Custom fields for auth and backend integration
  customFields: {
    betterAuthUrl: process.env.BETTER_AUTH_URL || 'http://localhost:3001',
    backendUrl: process.env.BACKEND_URL || 'http://localhost:8000',
    frontendUrl: process.env.FRONTEND_URL || 'http://localhost:3000',
  },

  // Client modules for initialization
  clientModules: [
    './src/clientModules/authInit.ts',
  ],

  plugins: [
    function (context, options) {
      return {
        name: 'custom-webpack-config',
        configureWebpack(config, isServer, utils) {
          return {
            resolve: {
              alias: {
                '@site': path.resolve(__dirname),
              },
              extensions: ['.ts', '.tsx', '.js', '.jsx', '.json'],
              modules: [
                path.resolve(__dirname, 'src'),
                'node_modules'
              ],
            },
          };
        },
      };
    },
  ],

  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
    localeConfigs: {
      en: {
        label: 'English',
        direction: 'ltr',
      },
      ur: {
        label: 'اردو',
        direction: 'rtl',
      },
    },
  },

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/',
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/saramali15792/physicalhumoniodbook/tree/main/intellistack/content/',
          showLastUpdateAuthor: true,
          showLastUpdateTime: true,
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/intellistack-social-card.jpg',
    navbar: {
      title: 'IntelliStack',
      logo: {
        alt: 'IntelliStack Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Curriculum',
        },
        {
          type: 'localeDropdown',
          position: 'right',
        },
        {
          href: 'https://github.com/saramali15792/physicalhumoniodbook',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Learn',
          items: [
            {
              label: 'Stage 1: Foundations',
              to: '/stage-1/intro',
            },
            {
              label: 'Stage 2: ROS 2',
              to: '/stage-2/intro',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/saramali15792/physicalhumoniodbook',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} IntelliStack. Built with Docusaurus.`,
    },
    prism: {
      theme: require('prism-react-renderer').themes.github,
      darkTheme: require('prism-react-renderer').themes.dracula,
      additionalLanguages: ['python', 'bash', 'yaml', 'json', 'cpp', 'cmake'],
    },
    mermaid: {
      theme: { light: 'neutral', dark: 'dark' },
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
