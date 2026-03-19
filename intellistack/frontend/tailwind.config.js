/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        /* Background */
        'bg-primary':    ({ opacityValue }) =>
          opacityValue !== undefined ? `rgba(10, 15, 30, ${opacityValue})` : '#0A0F1E',
        'bg-secondary': 'var(--color-bg-secondary)',
        'bg-tertiary':  'var(--color-bg-tertiary)',
        'bg-base':      'var(--color-bg-base)',
        'bg-elevated':  'var(--color-bg-elevated)',
        /* Accents */
        'accent-cyan':    'var(--color-accent-cyan)',
        'accent-blue':   ({ opacityValue }) =>
          opacityValue !== undefined ? `rgba(37, 99, 235, ${opacityValue})` : '#2563EB',
        'accent-blue-light': 'var(--color-accent-blue-light)',
        'accent-violet': ({ opacityValue }) =>
          opacityValue !== undefined ? `rgba(99, 102, 241, ${opacityValue})` : '#6366F1',
        'accent-amber':   'var(--color-accent-amber)',
        'accent-emerald': 'var(--color-accent-emerald)',
        'accent-teal':    'var(--color-accent-teal)',
        /* Text */
        'text-primary':   'var(--color-text-primary)',
        'text-secondary': 'var(--color-text-secondary)',
        'text-tertiary':  'var(--color-text-tertiary)',
        'text-muted':     'var(--color-text-muted)',
        /* Borders */
        'border-subtle':   'var(--color-border-subtle)',
        'border-default':  'var(--color-border-default)',
        'border-emphasis': 'var(--color-border-emphasis)',
      },
      spacing: {
        xs:   'var(--space-xs)',
        sm:   'var(--space-sm)',
        md:   'var(--space-md)',
        lg:   'var(--space-lg)',
        xl:   'var(--space-xl)',
        '2xl': 'var(--space-2xl)',
        '3xl': 'var(--space-3xl)',
      },
      fontFamily: {
        sans:    'var(--font-sans)',
        heading: 'var(--font-heading)',
        body:    'var(--font-body)',
        mono:    'var(--font-mono)',
      },
      fontSize: {
        xs:    'var(--text-xs)',
        sm:    'var(--text-sm)',
        base:  'var(--text-base)',
        lg:    'var(--text-lg)',
        xl:    'var(--text-xl)',
        '2xl': 'var(--text-2xl)',
        '3xl': 'var(--text-3xl)',
        '4xl': 'var(--text-4xl)',
        '5xl': 'var(--text-5xl)',
      },
      borderRadius: {
        sm:   'var(--radius-sm)',
        md:   'var(--radius-md)',
        lg:   'var(--radius-lg)',
        xl:   'var(--radius-xl)',
        full: 'var(--radius-full)',
      },
      boxShadow: {
        sm:              'var(--shadow-sm)',
        md:              'var(--shadow-md)',
        lg:              'var(--shadow-lg)',
        xl:              'var(--shadow-xl)',
        'glow-cyan':     'var(--shadow-glow-cyan)',
        'glow-blue':     'var(--shadow-glow-blue)',
        'glow-violet':   'var(--shadow-glow-violet)',
        'glow-amber':    'var(--shadow-glow-amber)',
        'glow-emerald':  'var(--shadow-glow-emerald)',
      },
      transitionDuration: {
        fast:   'var(--duration-fast)',
        normal: 'var(--duration-normal)',
        slow:   'var(--duration-slow)',
      },
      transitionTimingFunction: {
        linear:   'var(--ease-linear)',
        in:       'var(--ease-in)',
        out:      'var(--ease-out)',
        'in-out': 'var(--ease-in-out)',
        spring:   'var(--ease-spring)',
        smooth:   'var(--ease-smooth)',
      },
      keyframes: {
        'fade-up': {
          '0%':   { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'fade-in': {
          '0%':   { opacity: '0' },
          '100%': { opacity: '1' },
        },
        'entry-up': {
          '0%':   { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'typing-dot': {
          '0%, 80%, 100%': { transform: 'scale(0.6)', opacity: '0.4' },
          '40%':           { transform: 'scale(1)', opacity: '1' },
        },
        'fade-in-up': {
          '0%':   { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'slide-in-left': {
          '0%':   { opacity: '0', transform: 'translateX(-20px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
      },
      animation: {
        'fade-up':       'fade-up 0.5s var(--ease-smooth) both',
        'fade-in':       'fade-in 0.4s var(--ease-smooth) both',
        'entry-up':      'entry-up 0.5s var(--ease-smooth) both',
        'typing-dot':    'typing-dot 1.4s ease-in-out infinite',
        'fade-in-up':    'fade-in-up 0.5s var(--ease-smooth) both',
        'slide-in-left': 'slide-in-left 0.3s var(--ease-out) both',
      },
    },
  },
  plugins: [],
};
