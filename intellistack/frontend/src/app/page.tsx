import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800 text-white">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-20">
        <div className="text-center space-y-6">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
            IntelliStack
          </h1>
          <p className="text-xl text-slate-300 max-w-2xl mx-auto">
            Master Physical AI & Humanoid Robotics through structured,
            simulation-first learning with AI-powered tutoring
          </p>

          <div className="flex gap-4 justify-center pt-8">
            <Link
              href="/learn"
              className="px-8 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-medium transition-colors"
            >
              Start Learning
            </Link>
            <Link
              href="/login"
              className="px-8 py-3 border border-slate-600 hover:border-slate-500 rounded-lg font-medium transition-colors"
            >
              Sign In
            </Link>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-8 mt-20">
          <FeatureCard
            title="5-Stage Curriculum"
            description="Progress through Foundations, ROS 2, Perception & Planning, AI Integration, and Capstone projects"
            icon="📚"
          />
          <FeatureCard
            title="AI Tutor"
            description="Get Socratic guidance that helps you understand concepts without giving away answers"
            icon="🤖"
          />
          <FeatureCard
            title="Simulation First"
            description="Master robotics concepts safely in simulation before touching real hardware"
            icon="🎮"
          />
        </div>

        {/* Learning Path Preview */}
        <div className="mt-20">
          <h2 className="text-2xl font-bold text-center mb-10">
            Your Learning Journey
          </h2>
          <div className="flex justify-between items-center max-w-4xl mx-auto">
            {[
              { num: 1, name: "Foundations", status: "available" },
              { num: 2, name: "ROS 2 & Simulation", status: "locked" },
              { num: 3, name: "Perception", status: "locked" },
              { num: 4, name: "AI Integration", status: "locked" },
              { num: 5, name: "Capstone", status: "locked" },
            ].map((stage, i) => (
              <div key={stage.num} className="flex items-center">
                <div
                  className={`w-14 h-14 rounded-full flex items-center justify-center text-lg font-bold ${
                    stage.status === "available"
                      ? "bg-blue-600"
                      : "bg-slate-700"
                  }`}
                >
                  {stage.num}
                </div>
                {i < 4 && (
                  <div className="w-12 h-1 bg-slate-700 hidden md:block" />
                )}
              </div>
            ))}
          </div>
          <div className="flex justify-between max-w-4xl mx-auto mt-3">
            {["Foundations", "ROS 2", "Perception", "AI", "Capstone"].map(
              (name) => (
                <span
                  key={name}
                  className="text-xs text-slate-400 w-14 text-center"
                >
                  {name}
                </span>
              )
            )}
          </div>
        </div>
      </div>
    </main>
  );
}

function FeatureCard({
  title,
  description,
  icon,
}: {
  title: string;
  description: string;
  icon: string;
}) {
  return (
    <div className="p-6 rounded-xl bg-slate-800/50 border border-slate-700 hover:border-slate-600 transition-colors">
      <div className="text-4xl mb-4">{icon}</div>
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-slate-400 text-sm">{description}</p>
    </div>
  );
}
