"""
Pyodide Integration Helper
Client-side Python execution using Pyodide (WebAssembly)
Sprint 5: Interactive Code Blocks - Frontend Integration Guide
"""

# This file provides integration guidance for frontend developers
# Actual implementation will be in the frontend codebase

"""
PYODIDE INTEGRATION GUIDE
=========================

Pyodide allows running Python in the browser using WebAssembly.
This eliminates server load for basic Python code execution.

## Installation (Frontend)

```bash
npm install pyodide
```

## Basic Usage

```typescript
// Load Pyodide in a Web Worker for better performance
import { loadPyodide } from 'pyodide';

let pyodide = null;

async function initPyodide() {
  pyodide = await loadPyodide({
    indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/',
  });

  // Load common packages
  await pyodide.loadPackage(['numpy', 'pandas', 'matplotlib']);

  console.log('Pyodide ready');
}

async function runPythonCode(code: string): Promise<{output: string, error: string | null}> {
  if (!pyodide) {
    await initPyodide();
  }

  try {
    // Capture stdout
    pyodide.runPython(`
      import sys
      from io import StringIO
      sys.stdout = StringIO()
    `);

    // Run user code
    pyodide.runPython(code);

    // Get output
    const output = pyodide.runPython('sys.stdout.getvalue()');

    return { output, error: null };
  } catch (error) {
    return { output: '', error: error.message };
  }
}
```

## React Component Example

```typescript
import React, { useState, useEffect } from 'react';
import Editor from '@monaco-editor/react';

interface CodeEditorProps {
  initialCode: string;
  language: string;
  isEditable: boolean;
  isExecutable: boolean;
}

export const InteractiveCodeBlock: React.FC<CodeEditorProps> = ({
  initialCode,
  language,
  isEditable,
  isExecutable,
}) => {
  const [code, setCode] = useState(initialCode);
  const [output, setOutput] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleRun = async () => {
    setIsRunning(true);
    setOutput('');
    setError(null);

    try {
      if (language === 'python') {
        // Use Pyodide for Python
        const result = await runPythonCode(code);
        setOutput(result.output);
        setError(result.error);
      } else {
        // Use backend API for other languages
        const response = await fetch('/api/v1/code/execute', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            code,
            language,
            environment: 'docker',
          }),
        });

        const result = await response.json();
        setOutput(result.output);
        setError(result.error);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="code-block">
      <Editor
        height="300px"
        language={language}
        value={code}
        onChange={(value) => setCode(value || '')}
        options={{
          readOnly: !isEditable,
          minimap: { enabled: false },
          fontSize: 14,
          theme: 'vs-dark',
        }}
      />

      {isExecutable && (
        <button onClick={handleRun} disabled={isRunning}>
          {isRunning ? 'Running...' : 'Run Code'}
        </button>
      )}

      {output && (
        <pre className="output">
          {output}
        </pre>
      )}

      {error && (
        <pre className="error">
          {error}
        </pre>
      )}
    </div>
  );
};
```

## Web Worker Implementation (Recommended)

```typescript
// pyodide-worker.ts
import { loadPyodide } from 'pyodide';

let pyodide = null;

self.onmessage = async (event) => {
  const { id, code } = event.data;

  try {
    if (!pyodide) {
      pyodide = await loadPyodide();
      await pyodide.loadPackage(['numpy', 'pandas']);
    }

    // Capture stdout
    pyodide.runPython(`
      import sys
      from io import StringIO
      sys.stdout = StringIO()
    `);

    // Run code
    pyodide.runPython(code);

    // Get output
    const output = pyodide.runPython('sys.stdout.getvalue()');

    self.postMessage({ id, output, error: null });
  } catch (error) {
    self.postMessage({ id, output: '', error: error.message });
  }
};

// Main thread usage
const worker = new Worker(new URL('./pyodide-worker.ts', import.meta.url));

function runPythonInWorker(code: string): Promise<{output: string, error: string | null}> {
  return new Promise((resolve) => {
    const id = Math.random().toString(36);

    const handler = (event) => {
      if (event.data.id === id) {
        worker.removeEventListener('message', handler);
        resolve({ output: event.data.output, error: event.data.error });
      }
    };

    worker.addEventListener('message', handler);
    worker.postMessage({ id, code });
  });
}
```

## Terminal-Style Output Component

```typescript
import React from 'react';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import 'xterm/css/xterm.css';

export const TerminalOutput: React.FC<{ output: string }> = ({ output }) => {
  const terminalRef = React.useRef<HTMLDivElement>(null);
  const terminal = React.useRef<Terminal | null>(null);

  React.useEffect(() => {
    if (terminalRef.current && !terminal.current) {
      terminal.current = new Terminal({
        theme: {
          background: '#1e1e1e',
          foreground: '#d4d4d4',
        },
        fontSize: 14,
        fontFamily: 'JetBrains Mono, monospace',
      });

      const fitAddon = new FitAddon();
      terminal.current.loadAddon(fitAddon);
      terminal.current.open(terminalRef.current);
      fitAddon.fit();
    }

    if (terminal.current && output) {
      terminal.current.clear();
      terminal.current.write(output);
    }
  }, [output]);

  return <div ref={terminalRef} className="terminal-output" />;
};
```

## Security Considerations

1. **Input Validation**: Always validate code before execution
2. **Timeout**: Set execution timeout (30 seconds recommended)
3. **Memory Limits**: Pyodide runs in browser, limited by browser memory
4. **No File System**: Pyodide has no access to user's file system
5. **No Network**: Pyodide cannot make network requests by default

## Supported Packages

Pyodide supports many popular Python packages:
- numpy
- pandas
- matplotlib
- scipy
- scikit-learn
- sympy
- And many more...

Full list: https://pyodide.org/en/stable/usage/packages-in-pyodide.html

## Performance Tips

1. Load Pyodide once and reuse the instance
2. Use Web Workers to avoid blocking the main thread
3. Preload common packages during initialization
4. Cache Pyodide instance in service worker for faster subsequent loads

## Error Handling

```typescript
async function safePythonExecution(code: string) {
  try {
    // Validate code first
    const validation = await fetch('/api/v1/code/validate', {
      method: 'POST',
      body: JSON.stringify({ code, language: 'python' }),
    });

    const validationResult = await validation.json();

    if (!validationResult.valid) {
      return { output: '', error: validationResult.error };
    }

    // Execute if valid
    return await runPythonCode(code);
  } catch (error) {
    return { output: '', error: error.message };
  }
}
```

## Integration with Backend

For code that requires ROS 2 or system access, fall back to backend:

```typescript
async function executeCode(code: string, language: string) {
  // Use Pyodide for basic Python
  if (language === 'python' && !requiresROS2(code)) {
    return await runPythonCode(code);
  }

  // Use backend for ROS 2, Bash, C++
  const response = await fetch('/api/v1/code/execute', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      code,
      language,
      environment: 'docker',
    }),
  });

  return await response.json();
}

function requiresROS2(code: string): boolean {
  const ros2Imports = ['rclpy', 'rclcpp', 'ros2', 'tf2'];
  return ros2Imports.some(pkg => code.includes(pkg));
}
```

## Styling

```css
.code-block {
  border: 1px solid #333;
  border-radius: 8px;
  overflow: hidden;
  margin: 1rem 0;
}

.code-block button {
  background: #0066cc;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  cursor: pointer;
  font-size: 14px;
}

.code-block button:hover {
  background: #0052a3;
}

.code-block button:disabled {
  background: #666;
  cursor: not-allowed;
}

.output {
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 1rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  overflow-x: auto;
}

.error {
  background: #3d1f1f;
  color: #f48771;
  padding: 1rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  overflow-x: auto;
}

.terminal-output {
  height: 300px;
  background: #1e1e1e;
}
```

## Complete Example

See the full implementation example in the frontend codebase:
- `frontend/src/components/code/InteractiveCodeBlock.tsx`
- `frontend/src/workers/pyodide-worker.ts`
- `frontend/src/hooks/useCodeExecution.ts`

"""

# Backend API Integration Points
# ================================

# 1. Execute Code
# POST /api/v1/code/execute
# Body: { code, language, environment, timeout }
# Response: { output, error, execution_time, status }

# 2. Execute with Streaming
# POST /api/v1/code/execute/stream
# Returns: Server-Sent Events (SSE)
# Events: start, output, error, complete

# 3. Validate Code
# POST /api/v1/code/validate
# Body: { code, language }
# Response: { valid, error, warnings }

# 4. Get Execution Environments
# GET /api/v1/code/environments
# Response: [{ name, description, supported_languages, features, limitations }]

# 5. Get Code Blocks for Content
# GET /api/v1/code/code-blocks/{content_id}
# Response: { content_id, code_blocks: [...] }

# 6. Get Execution Stats
# GET /api/v1/code/stats
# Response: { executions_last_minute, rate_limit, remaining }
