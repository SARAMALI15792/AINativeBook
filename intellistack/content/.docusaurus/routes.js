import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/AINativeBook/__docusaurus/debug',
    component: ComponentCreator('/AINativeBook/__docusaurus/debug', 'f8a'),
    exact: true
  },
  {
    path: '/AINativeBook/__docusaurus/debug/config',
    component: ComponentCreator('/AINativeBook/__docusaurus/debug/config', 'c7f'),
    exact: true
  },
  {
    path: '/AINativeBook/__docusaurus/debug/content',
    component: ComponentCreator('/AINativeBook/__docusaurus/debug/content', '1d7'),
    exact: true
  },
  {
    path: '/AINativeBook/__docusaurus/debug/globalData',
    component: ComponentCreator('/AINativeBook/__docusaurus/debug/globalData', '0ab'),
    exact: true
  },
  {
    path: '/AINativeBook/__docusaurus/debug/metadata',
    component: ComponentCreator('/AINativeBook/__docusaurus/debug/metadata', '41f'),
    exact: true
  },
  {
    path: '/AINativeBook/__docusaurus/debug/registry',
    component: ComponentCreator('/AINativeBook/__docusaurus/debug/registry', 'd0a'),
    exact: true
  },
  {
    path: '/AINativeBook/__docusaurus/debug/routes',
    component: ComponentCreator('/AINativeBook/__docusaurus/debug/routes', '2b2'),
    exact: true
  },
  {
    path: '/AINativeBook/auth/callback',
    component: ComponentCreator('/AINativeBook/auth/callback', 'b30'),
    exact: true
  },
  {
    path: '/AINativeBook/auth/login',
    component: ComponentCreator('/AINativeBook/auth/login', '74a'),
    exact: true
  },
  {
    path: '/AINativeBook/auth/signup',
    component: ComponentCreator('/AINativeBook/auth/signup', '163'),
    exact: true
  },
  {
    path: '/AINativeBook/forgot-password',
    component: ComponentCreator('/AINativeBook/forgot-password', 'aa4'),
    exact: true
  },
  {
    path: '/AINativeBook/login',
    component: ComponentCreator('/AINativeBook/login', '273'),
    exact: true
  },
  {
    path: '/AINativeBook/onboarding/step-1',
    component: ComponentCreator('/AINativeBook/onboarding/step-1', '35a'),
    exact: true
  },
  {
    path: '/AINativeBook/onboarding/step-2',
    component: ComponentCreator('/AINativeBook/onboarding/step-2', '5a3'),
    exact: true
  },
  {
    path: '/AINativeBook/onboarding/step-3',
    component: ComponentCreator('/AINativeBook/onboarding/step-3', 'f75'),
    exact: true
  },
  {
    path: '/AINativeBook/onboarding/step-4',
    component: ComponentCreator('/AINativeBook/onboarding/step-4', 'b31'),
    exact: true
  },
  {
    path: '/AINativeBook/profile',
    component: ComponentCreator('/AINativeBook/profile', '265'),
    exact: true
  },
  {
    path: '/AINativeBook/register',
    component: ComponentCreator('/AINativeBook/register', '135'),
    exact: true
  },
  {
    path: '/AINativeBook/reset-password',
    component: ComponentCreator('/AINativeBook/reset-password', '4b0'),
    exact: true
  },
  {
    path: '/AINativeBook/settings',
    component: ComponentCreator('/AINativeBook/settings', 'ef6'),
    exact: true
  },
  {
    path: '/AINativeBook/',
    component: ComponentCreator('/AINativeBook/', '60b'),
    exact: true
  },
  {
    path: '/AINativeBook/',
    component: ComponentCreator('/AINativeBook/', 'e0d'),
    routes: [
      {
        path: '/AINativeBook/',
        component: ComponentCreator('/AINativeBook/', 'f34'),
        routes: [
          {
            path: '/AINativeBook/tags',
            component: ComponentCreator('/AINativeBook/tags', '5e1'),
            exact: true
          },
          {
            path: '/AINativeBook/tags/ext-4',
            component: ComponentCreator('/AINativeBook/tags/ext-4', 'e65'),
            exact: true
          },
          {
            path: '/AINativeBook/tags/file-systems',
            component: ComponentCreator('/AINativeBook/tags/file-systems', 'e95'),
            exact: true
          },
          {
            path: '/AINativeBook/tags/linux',
            component: ComponentCreator('/AINativeBook/tags/linux', '5ed'),
            exact: true
          },
          {
            path: '/AINativeBook/tags/preempt-rt',
            component: ComponentCreator('/AINativeBook/tags/preempt-rt', 'aa4'),
            exact: true
          },
          {
            path: '/AINativeBook/tags/processes',
            component: ComponentCreator('/AINativeBook/tags/processes', '62f'),
            exact: true
          },
          {
            path: '/AINativeBook/tags/real-time',
            component: ComponentCreator('/AINativeBook/tags/real-time', '492'),
            exact: true
          },
          {
            path: '/AINativeBook/tags/scheduling',
            component: ComponentCreator('/AINativeBook/tags/scheduling', 'de7'),
            exact: true
          },
          {
            path: '/AINativeBook/tags/storage',
            component: ComponentCreator('/AINativeBook/tags/storage', '672'),
            exact: true
          },
          {
            path: '/AINativeBook/tags/vfs',
            component: ComponentCreator('/AINativeBook/tags/vfs', 'fdd'),
            exact: true
          },
          {
            path: '/AINativeBook/',
            component: ComponentCreator('/AINativeBook/', '11a'),
            routes: [
              {
                path: '/AINativeBook/category/01-linux--systems',
                component: ComponentCreator('/AINativeBook/category/01-linux--systems', '145'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/category/01-the-distributed-mind',
                component: ComponentCreator('/AINativeBook/category/01-the-distributed-mind', '4f4'),
                exact: true,
                sidebar: "stage2Sidebar"
              },
              {
                path: '/AINativeBook/category/02-middleware--communication',
                component: ComponentCreator('/AINativeBook/category/02-middleware--communication', '7f6'),
                exact: true,
                sidebar: "stage2Sidebar"
              },
              {
                path: '/AINativeBook/category/02-python-internal-theory',
                component: ComponentCreator('/AINativeBook/category/02-python-internal-theory', '1a9'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/category/03-mathematics-of-reality',
                component: ComponentCreator('/AINativeBook/category/03-mathematics-of-reality', '202'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/category/03-services--actions',
                component: ComponentCreator('/AINativeBook/category/03-services--actions', '911'),
                exact: true,
                sidebar: "stage2Sidebar"
              },
              {
                path: '/AINativeBook/category/04-git--history',
                component: ComponentCreator('/AINativeBook/category/04-git--history', '3c9'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/category/04-tf2--transforms',
                component: ComponentCreator('/AINativeBook/category/04-tf2--transforms', '564'),
                exact: true,
                sidebar: "stage2Sidebar"
              },
              {
                path: '/AINativeBook/stage-1/1-1-linux-theory',
                component: ComponentCreator('/AINativeBook/stage-1/1-1-linux-theory', '264'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/stage-1/1-2-python-axioms',
                component: ComponentCreator('/AINativeBook/stage-1/1-2-python-axioms', '480'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/stage-1/1-3-async-theory',
                component: ComponentCreator('/AINativeBook/stage-1/1-3-async-theory', 'db8'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/stage-1/1-4-linear-algebra',
                component: ComponentCreator('/AINativeBook/stage-1/1-4-linear-algebra', 'b30'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/stage-1/1-6-git-history',
                component: ComponentCreator('/AINativeBook/stage-1/1-6-git-history', 'ddd'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/stage-1/1-7-bash-shell',
                component: ComponentCreator('/AINativeBook/stage-1/1-7-bash-shell', 'e8e'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/stage-1/git',
                component: ComponentCreator('/AINativeBook/stage-1/git', '835'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/stage-1/git/1-6-git-history',
                component: ComponentCreator('/AINativeBook/stage-1/git/1-6-git-history', 'af2'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/stage-1/intro',
                component: ComponentCreator('/AINativeBook/stage-1/intro', 'd0a'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/stage-1/linux',
                component: ComponentCreator('/AINativeBook/stage-1/linux', '66b'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/stage-1/linux-fundamentals',
                component: ComponentCreator('/AINativeBook/stage-1/linux-fundamentals', '66a'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/stage-1/linux/1-1-linux-theory',
                component: ComponentCreator('/AINativeBook/stage-1/linux/1-1-linux-theory', '50e'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/stage-1/linux/1-2-linux-file-systems',
                component: ComponentCreator('/AINativeBook/stage-1/linux/1-2-linux-file-systems', '31b'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/stage-1/linux/1-3-process-management',
                component: ComponentCreator('/AINativeBook/stage-1/linux/1-3-process-management', '2ca'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/stage-1/linux/1-7-bash-shell',
                component: ComponentCreator('/AINativeBook/stage-1/linux/1-7-bash-shell', 'd54'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/stage-1/math',
                component: ComponentCreator('/AINativeBook/stage-1/math', 'da6'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/stage-1/math-foundations',
                component: ComponentCreator('/AINativeBook/stage-1/math-foundations', '541'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/stage-1/math/1-4-linear-algebra',
                component: ComponentCreator('/AINativeBook/stage-1/math/1-4-linear-algebra', '1aa'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/stage-1/math/1-5-calculus-dynamics',
                component: ComponentCreator('/AINativeBook/stage-1/math/1-5-calculus-dynamics', '2c1'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/stage-1/physics-basics',
                component: ComponentCreator('/AINativeBook/stage-1/physics-basics', '900'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/stage-1/python',
                component: ComponentCreator('/AINativeBook/stage-1/python', 'd4c'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/stage-1/python-basics',
                component: ComponentCreator('/AINativeBook/stage-1/python-basics', 'ec2'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/stage-1/python/1-2-python-axioms',
                component: ComponentCreator('/AINativeBook/stage-1/python/1-2-python-axioms', 'a3f'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/stage-1/python/1-3-async-theory',
                component: ComponentCreator('/AINativeBook/stage-1/python/1-3-async-theory', 'f60'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/stage-1/theory/1-1-axioms-computation',
                component: ComponentCreator('/AINativeBook/stage-1/theory/1-1-axioms-computation', 'c33'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/AINativeBook/stage-2/gazebo-simulation',
                component: ComponentCreator('/AINativeBook/stage-2/gazebo-simulation', 'e8d'),
                exact: true,
                sidebar: "stage2Sidebar"
              },
              {
                path: '/AINativeBook/stage-2/graph-theory/2-1-distributed-mind',
                component: ComponentCreator('/AINativeBook/stage-2/graph-theory/2-1-distributed-mind', '315'),
                exact: true,
                sidebar: "stage2Sidebar"
              },
              {
                path: '/AINativeBook/stage-2/intro',
                component: ComponentCreator('/AINativeBook/stage-2/intro', '44f'),
                exact: true,
                sidebar: "stage2Sidebar"
              },
              {
                path: '/AINativeBook/stage-2/middleware/2-2-pub-sub',
                component: ComponentCreator('/AINativeBook/stage-2/middleware/2-2-pub-sub', '400'),
                exact: true,
                sidebar: "stage2Sidebar"
              },
              {
                path: '/AINativeBook/stage-2/ros2-setup',
                component: ComponentCreator('/AINativeBook/stage-2/ros2-setup', '4e6'),
                exact: true,
                sidebar: "stage2Sidebar"
              },
              {
                path: '/AINativeBook/stage-2/services/2-3-services-actions',
                component: ComponentCreator('/AINativeBook/stage-2/services/2-3-services-actions', 'e2a'),
                exact: true,
                sidebar: "stage2Sidebar"
              },
              {
                path: '/AINativeBook/stage-2/tf2/2-4-coordinate-frames',
                component: ComponentCreator('/AINativeBook/stage-2/tf2/2-4-coordinate-frames', '91f'),
                exact: true,
                sidebar: "stage2Sidebar"
              },
              {
                path: '/AINativeBook/stage-3/computer-vision',
                component: ComponentCreator('/AINativeBook/stage-3/computer-vision', 'd25'),
                exact: true,
                sidebar: "stage3Sidebar"
              },
              {
                path: '/AINativeBook/stage-3/intro',
                component: ComponentCreator('/AINativeBook/stage-3/intro', '899'),
                exact: true,
                sidebar: "stage3Sidebar"
              },
              {
                path: '/AINativeBook/stage-4/intro',
                component: ComponentCreator('/AINativeBook/stage-4/intro', 'fe0'),
                exact: true,
                sidebar: "stage4Sidebar"
              },
              {
                path: '/AINativeBook/stage-4/machine-learning-basics',
                component: ComponentCreator('/AINativeBook/stage-4/machine-learning-basics', '258'),
                exact: true,
                sidebar: "stage4Sidebar"
              },
              {
                path: '/AINativeBook/stage-5/intro',
                component: ComponentCreator('/AINativeBook/stage-5/intro', '340'),
                exact: true,
                sidebar: "stage5Sidebar"
              },
              {
                path: '/AINativeBook/stage-5/project-guidelines',
                component: ComponentCreator('/AINativeBook/stage-5/project-guidelines', 'b65'),
                exact: true,
                sidebar: "stage5Sidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
