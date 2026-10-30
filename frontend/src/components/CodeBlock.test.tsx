import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { CodeBlock } from './CodeBlock';

describe('CodeBlock Component with Auto-Detection', () => {
  it('detects Golang code automatically', () => {
    const goCode = `package main

import "fmt"

func main() {
    ch := make(chan int, 5)
    go func() {
        ch <- 42
    }()
    val := <-ch
    fmt.Printf("Received: %d\\n", val)
}`;

    render(<CodeBlock code={goCode} />);

    // Should detect Go and display Go badge
    expect(screen.getByText('Go (Golang)')).toBeInTheDocument();
    expect(screen.getByText('Копировать')).toBeInTheDocument();
  });

  it('detects Python code automatically', () => {
    const pythonCode = `import asyncio

async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()`;

    render(<CodeBlock code={pythonCode} />);

    // Should detect Python and display Python badge
    expect(screen.getByText('Python')).toBeInTheDocument();
  });

  it('copies code to clipboard and updates button state', async () => {
    const code = 'const greeting = "Hello, world!";';
    render(<CodeBlock code={code} language="typescript" />);

    const copyBtn = screen.getByText('Копировать').closest('button');
    expect(copyBtn).toBeInTheDocument();

    fireEvent.click(copyBtn!);
    expect(navigator.clipboard.writeText).toHaveBeenCalledWith(code);

    expect(await screen.findByText('Скопировано')).toBeInTheDocument();
  });
});
