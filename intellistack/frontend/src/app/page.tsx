import Link from "next/link";
import {
  BookOpen,
  Bot,
  MessageSquare,
  ClipboardCheck,
  Users,
  Award,
  ArrowRight,
  ChevronRight,
  Star,
} from "lucide-react";

const features = [
  {
    icon: BookOpen,
    title: "5-Stage Learning Path",
    description:
      "Progress through Foundations, ROS 2, Perception & Planning, AI Integration, and a hands-on Capstone project.",
  },
  {
    icon: Bot,
    title: "AI Tutor",
    description:
      "Socratic guidance that helps you understand concepts deeply without giving away answers.",
  },
  {
    icon: MessageSquare,
    title: "RAG Chatbot",
    description:
      "AI-powered chatbot with citation support, drawing from course materials and documentation.",
  },
  {
    icon: ClipboardCheck,
    title: "Assessments",
    description:
      "Quiz delivery with rubric-based grading to verify your understanding at every stage.",
  },
  {
    icon: Users,
    title: "Community",
    description:
      "Forums, study groups, and mentorship to learn alongside fellow robotics enthusiasts.",
  },
  {
    icon: Award,
    title: "Certificates & Badges",
    description:
      "Earn verifiable certificates and badges as you complete stages and demonstrate mastery.",
  },
];

const stages = [
  { num: 1, name: "Foundations", desc: "Math, physics, and programming basics" },
  { num: 2, name: "ROS 2 & Simulation", desc: "Gazebo, Isaac Sim, ROS 2 core" },
  { num: 3, name: "Perception & Planning", desc: "Computer vision, SLAM, navigation" },
  { num: 4, name: "AI Integration", desc: "ML models, reinforcement learning" },
  { num: 5, name: "Capstone Project", desc: "Build your own humanoid robot system" },
];

const testimonials = [
  {
    name: "Dr. Sarah Chen",
    role: "Robotics Researcher, MIT",
    quote:
      "IntelliStack's structured approach to physical AI education is exactly what the industry needed. The simulation-first methodology ensures students build real intuition.",
    avatar: "SC",
  },
  {
    name: "James Okafor",
    role: "Graduate Student, Stanford",
    quote:
      "The AI tutor helped me understand ROS 2 concepts I'd been struggling with for months. The Socratic approach made everything click.",
    avatar: "JO",
  },
  {
    name: "Maria Rodriguez",
    role: "Senior Engineer, Boston Dynamics",
    quote:
      "I recommend IntelliStack to every aspiring roboticist. The curriculum is rigorous, practical, and beautifully organized.",
    avatar: "MR",
  },
];

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-background font-sans">
      {/* Navbar */}
      <header className="sticky top-0 z-50 bg-card/95 backdrop-blur-sm border-b border-border">
        <div className="container mx-auto px-4">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-primary-400 flex items-center justify-center shadow-md border border-primary-600">
                <span className="text-white text-lg font-bold">IS</span>
              </div>
              <div>
                <h1 className="text-xl font-bold text-foreground font-serif m-0">
                  IntelliStack
                </h1>
                <p className="text-xs text-secondary -mt-0.5 font-medium m-0">
                  Physical AI & Humanoid Robotics
                </p>
              </div>
            </div>
            <nav className="hidden md:flex items-center gap-6">
              <a href="#features" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                Features
              </a>
              <a href="#curriculum" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                Curriculum
              </a>
              <a href="#testimonials" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                Testimonials
              </a>
              <a href="#pricing" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                Pricing
              </a>
            </nav>
            <div className="flex items-center gap-3">
              <Link
                href="/login"
                className="text-sm font-medium text-foreground hover:text-primary transition-colors"
              >
                Sign In
              </Link>
              <Link
                href="/register"
                className="px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:bg-primary-600 transition-colors shadow-sm"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative overflow-hidden paper-texture">
        <div className="container mx-auto px-4 py-20 md:py-32">
          <div className="max-w-3xl mx-auto text-center relative z-10">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-muted border border-border text-sm text-muted-foreground mb-6">
              <Star className="w-4 h-4 text-primary" />
              <span>Now in Early Access</span>
            </div>
            <h1 className="text-4xl md:text-6xl font-bold text-foreground font-serif tracking-tight leading-tight mb-6">
              Master Physical AI &{" "}
              <span className="text-primary">Humanoid Robotics</span>
            </h1>
            <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto mb-10 leading-relaxed">
              A structured, simulation-first learning platform with AI-powered
              tutoring, progressive curricula, and hands-on projects. From
              foundations to building your own humanoid robot systems.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/register"
                className="inline-flex items-center justify-center gap-2 px-8 py-3.5 bg-primary text-primary-foreground rounded-lg text-base font-semibold hover:bg-primary-600 transition-colors shadow-book"
              >
                Start Learning
                <ArrowRight className="w-5 h-5" />
              </Link>
              <a
                href="#curriculum"
                className="inline-flex items-center justify-center gap-2 px-8 py-3.5 border-2 border-border text-foreground rounded-lg text-base font-semibold hover:bg-muted transition-colors"
              >
                Explore Curriculum
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section id="features" className="py-20 bg-card">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground font-serif mb-4">
              Everything You Need to Master Robotics
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              A comprehensive platform designed by roboticists, for roboticists.
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {features.map((feature) => (
              <div
                key={feature.title}
                className="p-6 rounded-xl bg-background border border-border hover:border-primary/30 hover:shadow-book transition-all group"
              >
                <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4 group-hover:bg-primary/20 transition-colors">
                  <feature.icon className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-lg font-semibold text-foreground font-serif mb-2">
                  {feature.title}
                </h3>
                <p className="text-sm text-muted-foreground leading-relaxed m-0">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Learning Path Preview */}
      <section id="curriculum" className="py-20 bg-background paper-texture">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16 relative z-10">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground font-serif mb-4">
              Your Learning Journey
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Five progressive stages from foundations to building your own
              humanoid robot system.
            </p>
          </div>

          <div className="max-w-4xl mx-auto relative z-10">
            {/* Desktop Timeline */}
            <div className="hidden md:block">
              <div className="flex items-start justify-between relative">
                {/* Connection line */}
                <div className="absolute top-7 left-[10%] right-[10%] h-0.5 bg-border" />
                {stages.map((stage) => (
                  <div key={stage.num} className="flex flex-col items-center text-center w-1/5 relative">
                    <div className="w-14 h-14 rounded-full bg-card border-2 border-primary flex items-center justify-center text-lg font-bold text-primary shadow-sm z-10">
                      {stage.num}
                    </div>
                    <h4 className="mt-3 text-sm font-semibold text-foreground">
                      {stage.name}
                    </h4>
                    <p className="mt-1 text-xs text-muted-foreground m-0">
                      {stage.desc}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Mobile List */}
            <div className="md:hidden space-y-4">
              {stages.map((stage, i) => (
                <div
                  key={stage.num}
                  className="flex items-start gap-4 p-4 bg-card rounded-xl border border-border"
                >
                  <div className="flex-shrink-0 w-10 h-10 rounded-full bg-primary/10 border-2 border-primary flex items-center justify-center text-sm font-bold text-primary">
                    {stage.num}
                  </div>
                  <div>
                    <h4 className="font-semibold text-foreground text-sm m-0">
                      Stage {stage.num}: {stage.name}
                    </h4>
                    <p className="text-xs text-muted-foreground mt-1 m-0">
                      {stage.desc}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section id="testimonials" className="py-20 bg-card">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground font-serif mb-4">
              Trusted by Roboticists Worldwide
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Hear from students and professionals who transformed their careers.
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {testimonials.map((t) => (
              <div
                key={t.name}
                className="p-6 rounded-xl bg-background border border-border"
              >
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-primary-400 flex items-center justify-center text-sm font-bold text-white">
                    {t.avatar}
                  </div>
                  <div>
                    <p className="font-semibold text-foreground text-sm m-0">
                      {t.name}
                    </p>
                    <p className="text-xs text-muted-foreground m-0">{t.role}</p>
                  </div>
                </div>
                <p className="text-sm text-muted-foreground italic leading-relaxed m-0">
                  &ldquo;{t.quote}&rdquo;
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="py-20 bg-background paper-texture">
        <div className="container mx-auto px-4 relative z-10">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground font-serif mb-4">
              Simple, Transparent Pricing
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Start for free and upgrade when you&apos;re ready.
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
            {/* Free */}
            <div className="p-6 rounded-xl bg-card border border-border">
              <h3 className="text-lg font-semibold text-foreground font-serif mb-1">
                Free
              </h3>
              <p className="text-muted-foreground text-sm mb-4">
                Get started with the basics
              </p>
              <p className="text-3xl font-bold text-foreground mb-6">
                $0
                <span className="text-sm font-normal text-muted-foreground">
                  /month
                </span>
              </p>
              <ul className="space-y-2 mb-6">
                {["Stage 1: Foundations", "Community access", "Basic AI chatbot"].map(
                  (item) => (
                    <li key={item} className="flex items-center gap-2 text-sm text-muted-foreground">
                      <ChevronRight className="w-4 h-4 text-primary flex-shrink-0" />
                      {item}
                    </li>
                  )
                )}
              </ul>
              <Link
                href="/register"
                className="block w-full text-center py-2.5 rounded-lg border-2 border-border text-foreground font-medium text-sm hover:bg-muted transition-colors"
              >
                Get Started Free
              </Link>
            </div>

            {/* Pro */}
            <div className="p-6 rounded-xl bg-card border-2 border-primary shadow-book relative">
              <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-0.5 bg-primary text-primary-foreground text-xs font-semibold rounded-full">
                Popular
              </div>
              <h3 className="text-lg font-semibold text-foreground font-serif mb-1">
                Pro
              </h3>
              <p className="text-muted-foreground text-sm mb-4">
                Full access for serious learners
              </p>
              <p className="text-3xl font-bold text-foreground mb-6">
                $29
                <span className="text-sm font-normal text-muted-foreground">
                  /month
                </span>
              </p>
              <ul className="space-y-2 mb-6">
                {[
                  "All 5 learning stages",
                  "AI Tutor (unlimited)",
                  "Assessments & certificates",
                  "Priority community support",
                ].map((item) => (
                  <li key={item} className="flex items-center gap-2 text-sm text-muted-foreground">
                    <ChevronRight className="w-4 h-4 text-primary flex-shrink-0" />
                    {item}
                  </li>
                ))}
              </ul>
              <Link
                href="/register"
                className="block w-full text-center py-2.5 rounded-lg bg-primary text-primary-foreground font-medium text-sm hover:bg-primary-600 transition-colors"
              >
                Start Pro Trial
              </Link>
            </div>

            {/* Institution */}
            <div className="p-6 rounded-xl bg-card border border-border">
              <h3 className="text-lg font-semibold text-foreground font-serif mb-1">
                Institution
              </h3>
              <p className="text-muted-foreground text-sm mb-4">
                For universities and teams
              </p>
              <p className="text-3xl font-bold text-foreground mb-6">
                Custom
              </p>
              <ul className="space-y-2 mb-6">
                {[
                  "Everything in Pro",
                  "Cohort management",
                  "Analytics dashboard",
                  "Custom integrations",
                ].map((item) => (
                  <li key={item} className="flex items-center gap-2 text-sm text-muted-foreground">
                    <ChevronRight className="w-4 h-4 text-primary flex-shrink-0" />
                    {item}
                  </li>
                ))}
              </ul>
              <Link
                href="/register"
                className="block w-full text-center py-2.5 rounded-lg border-2 border-border text-foreground font-medium text-sm hover:bg-muted transition-colors"
              >
                Contact Sales
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 bg-gradient-to-r from-primary to-primary-400">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white font-serif mb-4">
            Ready to Begin Your Journey?
          </h2>
          <p className="text-lg text-white/80 max-w-xl mx-auto mb-8">
            Join thousands of roboticists building the future of physical AI.
            Start with the fundamentals and work your way to mastery.
          </p>
          <Link
            href="/register"
            className="inline-flex items-center gap-2 px-8 py-3.5 bg-white text-primary rounded-lg text-base font-semibold hover:bg-white/90 transition-colors shadow-lg"
          >
            Create Free Account
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-secondary-800 text-secondary-200">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            {/* Brand */}
            <div>
              <div className="flex items-center gap-2 mb-4">
                <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center">
                  <span className="text-white text-sm font-bold">IS</span>
                </div>
                <span className="text-white font-serif font-bold">IntelliStack</span>
              </div>
              <p className="text-sm text-secondary-400 m-0">
                AI-Native Learning Platform for Physical AI & Humanoid Robotics.
              </p>
            </div>

            {/* Platform */}
            <div>
              <h4 className="text-white font-semibold mb-3 text-sm">Platform</h4>
              <ul className="space-y-2">
                {["Learning Path", "AI Tutor", "Assessments", "Community"].map(
                  (item) => (
                    <li key={item}>
                      <Link href="/learn" className="text-sm text-secondary-400 hover:text-white transition-colors">
                        {item}
                      </Link>
                    </li>
                  )
                )}
              </ul>
            </div>

            {/* Resources */}
            <div>
              <h4 className="text-white font-semibold mb-3 text-sm">Resources</h4>
              <ul className="space-y-2">
                {["Documentation", "API Reference", "Blog", "Changelog"].map(
                  (item) => (
                    <li key={item}>
                      <span className="text-sm text-secondary-400">{item}</span>
                    </li>
                  )
                )}
              </ul>
            </div>

            {/* Legal */}
            <div>
              <h4 className="text-white font-semibold mb-3 text-sm">Legal</h4>
              <ul className="space-y-2">
                {["Terms of Service", "Privacy Policy", "Cookie Policy"].map(
                  (item) => (
                    <li key={item}>
                      <span className="text-sm text-secondary-400">{item}</span>
                    </li>
                  )
                )}
              </ul>
            </div>
          </div>

          <div className="border-t border-secondary-700 pt-8 text-center">
            <p className="text-sm text-secondary-500 m-0">
              &copy; {new Date().getFullYear()} IntelliStack. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </main>
  );
}
