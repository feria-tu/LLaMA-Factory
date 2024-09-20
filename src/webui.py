# Copyright 2024 the LlamaFactory team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from llamafactory.webui.interface import create_ui


def main():
    print(f"GRADIO_SHARE: {os.environ.get('GRADIO_SHARE', '0')}")
    print(f"GRADIO_SERVER_NAME: {os.environ.get('GRADIO_SERVER_NAME', '0.0.0.0')}")
    print(f"GRADIO_SERVER_PORT: {os.environ.get('GRADIO_SERVER_PORT', '8080')}")
    
    gradio_share = os.environ.get("GRADIO_SHARE", "0").lower() in ["true", "1"]
    server_name = os.environ.get("GRADIO_SERVER_NAME", "0.0.0.0")
    server_port = int(os.environ.get("GRADIO_SERVER_PORT", "8080"))
    print(f"Launching LlamaFactory WebUI on {server_name}:{server_port}")
    create_ui().queue().launch(share=gradio_share, server_name=server_name, server_port=server_port, inbrowser=True)


if __name__ == "__main__":
    main()
