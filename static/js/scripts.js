document.getElementById("send-btn").addEventListener("click", async () => {
  const userInput = document.getElementById("user-input").value;
  const responseDiv = document.getElementById("response");

  if (!userInput) {
      responseDiv.textContent = "입력을 비워둘 수 없습니다.";
      return;
  }

  try {
      const res = await fetch("/api/search_learn", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: userInput })
      });

      const data = await res.json();
      if (data.error) {
          responseDiv.textContent = `오류: ${data.error}`;
      } else {
          responseDiv.innerHTML = `
              <p><strong>제목:</strong> ${data.title}</p>
              <p><strong>요약:</strong> ${data.summary}</p>
              <p><a href="${data.link}" target="_blank">자세히 보기</a></p>
          `;
      }
  } catch (error) {
      responseDiv.textContent = "요청 중 오류가 발생했습니다.";
  }
});
