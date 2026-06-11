import ReactMarkdown from "react-markdown";
import rehypeHighlight from "rehype-highlight";
import "highlight.js/styles/github-dark.css";

export default function MarkdownRender({ children }) {
  return (
    <ReactMarkdown rehypePlugins={[rehypeHighlight]}>
      {children}
    </ReactMarkdown>
  );
}
