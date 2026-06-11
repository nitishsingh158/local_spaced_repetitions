import { useEffect, useRef } from "react";
import { EditorView, basicSetup } from "codemirror";
import { EditorState } from "@codemirror/state";
import { python } from "@codemirror/lang-python";
import { sql } from "@codemirror/lang-sql";
import { oneDark } from "@codemirror/theme-one-dark";

function getLang(language) {
  if (language === "python") return python();
  if (language === "sql") return sql();
  return [];
}

export default function Scratchpad({ language, resetKey }) {
  const containerRef = useRef(null);
  const viewRef = useRef(null);

  useEffect(() => {
    if (viewRef.current) {
      viewRef.current.destroy();
    }
    viewRef.current = new EditorView({
      state: EditorState.create({
        doc: "",
        extensions: [basicSetup, oneDark, getLang(language)],
      }),
      parent: containerRef.current,
    });
    return () => viewRef.current?.destroy();
  }, [language, resetKey]);

  return <div ref={containerRef} className="scratchpad" />;
}
