import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import API from "../../api/resumeApi";

import { PieChart, Pie, Cell, Tooltip } from "recharts";

function ResumeUpload() {

  const [fileName, setFileName] = useState("");
  const [atsScore, setAtsScore] = useState(0);
  const [skills, setSkills] = useState([]);
  const [missingSkills, setMissingSkills] = useState([]);
  const [resumeText, setResumeText] = useState("");

  const [recommendedJobs, setRecommendedJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);
  const [suggestions, setSuggestions] = useState([]);

  const onDrop = useCallback(async (files) => {

    const file = files[0];
    if (!file) return;

    setFileName(file.name);

    const formData = new FormData();
    formData.append("resume", file);
    formData.append("role", "Data Scientist");

    try {

      const res = await API.post("/upload-resume", formData);

      setAtsScore(res.data.ats_score || 0);
      setSkills(res.data.skills || []);
      setMissingSkills(res.data.missing_skills || []);
      setResumeText(res.data.resume_text || "");
      setRecommendedJobs(res.data.recommended_jobs || []);
      setSuggestions(res.data.suggestions || []);

    } catch (err) {
      alert("Upload Failed");
    }

  }, []);

  const { getRootProps, getInputProps } = useDropzone({
    accept: { "application/pdf": [".pdf"] },
    onDrop
  });

  const skillData = [
    { name: "Matched", value: skills.length },
    { name: "Missing", value: missingSkills.length }
  ];

  return (

    <div className="min-h-screen bg-black text-white p-6">

      <h1 className="text-4xl text-center mb-6 font-bold">
        AI Resume Analyzer Dashboard
      </h1>

      {/* UPLOAD */}
      <div {...getRootProps()} className="border-2 border-dashed p-8 text-center rounded-xl mb-6">
        <input {...getInputProps()} />
        <p>Drag & Drop Resume PDF</p>
        {fileName && <p className="text-green-400">{fileName}</p>}
      </div>

      {/* DASHBOARD */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        {/* LEFT */}
        <div className="bg-zinc-900 p-6 rounded-2xl">

          <h2 className="text-2xl mb-4">Analysis</h2>

          <p className="text-green-400 text-3xl">{atsScore}/100 ATS</p>

          <div className="mt-4">
            <PieChart width={200} height={200}>
              <Pie data={skillData} dataKey="value" outerRadius={80}>
                <Cell fill="green" />
                <Cell fill="red" />
              </Pie>
              <Tooltip />
            </PieChart>
          </div>

          <h3 className="mt-4">Skills</h3>
          <div className="flex flex-wrap gap-2">
            {skills.map((s, i) => (
              <span key={i} className="bg-purple-600 px-2 py-1 rounded-full">
                {s}
              </span>
            ))}
          </div>

          <h3 className="mt-4">Missing</h3>
          <div className="flex flex-wrap gap-2">
            {missingSkills.map((s, i) => (
              <span key={i} className="bg-red-600 px-2 py-1 rounded-full">
                {s}
              </span>
            ))}
          </div>

        </div>

        {/* RIGHT */}
        <div className="bg-zinc-900 p-6 rounded-2xl">

          <h2 className="text-2xl mb-4">Jobs & AI Suggestions</h2>

          {/* JOBS */}
          <div className="flex flex-wrap gap-3">
            {recommendedJobs.map((job, i) => (
              <button
                key={i}
                onClick={() => setSelectedJob(job)}
                className="bg-blue-600 px-3 py-1 rounded-xl"
              >
                {job.role} ({job.match}%)
              </button>
            ))}
          </div>

          {/* SELECTED JOB */}
          {selectedJob && (
            <div className="mt-4 bg-zinc-800 p-3 rounded-xl">
              <h3>{selectedJob.role}</h3>
              <div className="flex flex-wrap gap-2">
                {selectedJob.skills.map((s, i) => (
                  <span key={i} className="bg-yellow-600 px-2 py-1 rounded-full">
                    {s}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* AI SUGGESTIONS */}
          <div className="mt-6">
            <h3 className="text-xl mb-2">AI Suggestions</h3>
            {suggestions.map((s, i) => (
              <p key={i} className="text-yellow-400">
                • {s}
              </p>
            ))}
          </div>

        </div>

      </div>

      {/* RESUME TEXT */}
      {resumeText && (
        <div className="mt-6 bg-zinc-900 p-4 rounded-xl">
          <h2>Resume Text</h2>
          <p className="text-sm whitespace-pre-wrap">{resumeText}</p>
        </div>
      )}

    </div>
  );
}

export default ResumeUpload;