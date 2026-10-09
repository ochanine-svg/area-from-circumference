
from manim import *
import math
import numpy as np


class AreaFromCircumference(Scene):
    def construct(self):
        r = 2
        center_shift = LEFT * 0.8 + UP * 0.4

        self.camera.background_color = WHITE

        poly_color = "#0000FF"
        highlight_color = BLUE
        final_fill_color = "#E8E8E8"

        Text.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)
        Tex.set_default(color=BLACK)
        Line.set_default(color=poly_color)

        # --------------------------------------------------
        # Helper functions
        # --------------------------------------------------

        def polygon_vertices(n):
            R = r / math.cos(math.pi / n)

            return [
                np.array([
                    R * math.cos((2*k + 1)*math.pi/n),
                    R * math.sin((2*k + 1)*math.pi/n),
                    0
                ])
                for k in range(n)
            ]

        def make_polygon(n):
            return Polygon(
                *polygon_vertices(n),
                color=poly_color,
                fill_opacity=0
            ).shift(center_shift)

        def make_polygon_fill(n):
            return Polygon(
                *polygon_vertices(n),
                stroke_width=0,
                fill_color=highlight_color,
                fill_opacity=0.18
            ).shift(center_shift)

        def make_spokes(n):
            verts = polygon_vertices(n)

            return VGroup(*[
                Line(
                    ORIGIN, v,
                    color=GRAY,
                    stroke_width=1.5
                )
                for v in verts
            ]).shift(center_shift)

        def make_highlight_triangle(n):
            verts = polygon_vertices(n)

            fill = Polygon(
                ORIGIN,
                verts[-1],
                verts[0],
                stroke_width=0,
                fill_color=highlight_color,
                fill_opacity=0.18
            )

            radial_1 = Line(
                ORIGIN,
                verts[-1],
                color=highlight_color
            )

            radial_2 = Line(
                ORIGIN,
                verts[0],
                color=highlight_color
            )

            outer_edge = Line(
                verts[-1],
                verts[0],
                color=poly_color
            )

            return VGroup(
                fill,
                radial_1,
                radial_2,
                outer_edge
            ).shift(center_shift)

        def make_triangle_fill(n, k):
            verts = polygon_vertices(n)

            return Polygon(
                ORIGIN,
                verts[k % n],
                verts[(k + 1) % n],
                stroke_width=0,
                fill_color=highlight_color,
                fill_opacity=0.18
            ).shift(center_shift)

        def make_x_label(n):
            verts = polygon_vertices(n)
            midpoint = (verts[-1] + verts[0]) / 2

            label = MathTex(
                "s",
                font_size=36
            ).move_to(
                midpoint + RIGHT * 0.15
            ).shift(center_shift)

            label.set_color(poly_color)

            return label

        def make_r_line():
            return Line(
                ORIGIN,
                RIGHT * r,
                color=highlight_color
            ).shift(center_shift)

        def make_r_label():
            return MathTex(
                "r",
                font_size=36
            ).move_to(
                RIGHT * 7*r/10 + DOWN * 0.15
            ).shift(center_shift)

        def place_formula(mob, shift_left=0.8):
            return mob.to_edge(
                DOWN,
                buff=0.35
            ).shift(
                LEFT * shift_left + UP * 0.35
            )

        def color_area(formula, index=0):
            formula[index].set_color(highlight_color)

        # --------------------------------------------------
        # Opening title
        # --------------------------------------------------

        title = Text(
            "Area of Circle from Circumference",
            font_size=42
        ).to_edge(UP).shift(LEFT * 0.8)

        self.play(
            Write(title),
            run_time=0.8
        )

        self.play(
            title.animate.scale(0.8)
            .set_opacity(0)
            .to_edge(UP, buff=0.25),
            run_time=0.6
        )

        # --------------------------------------------------
        # Initial circle and hexagon
        # --------------------------------------------------

        circle = Circle(
            radius=r,
            color=BLACK,
            stroke_width=2.72
        ).shift(center_shift)

        polygon = make_polygon(6)
        spokes = make_spokes(6)
        triangle = make_highlight_triangle(6)
        polygon_fill = make_polygon_fill(6)

        x_label = make_x_label(6)
        r_line = make_r_line()
        r_label = make_r_label()

        # --------------------------------------------------
        # Side panel: 6 equal sides
        # --------------------------------------------------

        verts = polygon.get_vertices()

        edge_length = np.linalg.norm(
            verts[1] - verts[0]
        )

        polygon_edge = Line(
            LEFT * edge_length / 2,
            RIGHT * edge_length / 2,
            color=poly_color,
            stroke_width=polygon.get_stroke_width()
        )

        edge_x = MathTex(
            "s",
            font_size=60,
            color=poly_color
        ).next_to(
            polygon_edge,
            UP,
            buff=0.1
        )

        six_sides_text = Text(
            "6 equal sides",
            font_size=30,
            color=BLACK
        )

        side_panel = VGroup(
            polygon_edge,
            edge_x,
            six_sides_text
        )

        six_sides_text.next_to(
            VGroup(polygon_edge, edge_x),
            DOWN,
            buff=0.28
        )

        side_panel.to_edge(
            RIGHT,
            buff=1.1
        ).shift(
            LEFT * 0.5 + UP * 1.45
        )

        # --------------------------------------------------
        # Draw circle, hexagon, side panel, spokes
        # --------------------------------------------------

        self.play(
            Create(circle),
            run_time=0.45
        )

        self.play(
            Create(polygon),
            run_time=1.0
        )

        self.wait(0.25)

        self.play(
            FadeIn(side_panel, shift=UP * 0.12),
            run_time=0.65
        )

        self.wait(0.65)

        self.play(
            Create(spokes),
            run_time=0.7
        )

        self.wait(0.4)

        self.play(
            FadeOut(side_panel),
            run_time=0.3
        )

        self.play(
            FadeIn(triangle),
            Write(x_label),
            Create(r_line),
            Write(r_label),
            run_time=0.85
        )

        self.wait(0.25)

        # --------------------------------------------------
        # Triangle area
        # --------------------------------------------------

        formula = MathTex(
            r"A",
            r"=",
            r"\frac{1}{2}",
            r"r",
            r"s",
            font_size=60
        )

        place_formula(formula)
        color_area(formula)
        formula[4].set_color(poly_color)

        self.play(
            Write(formula),
            run_time=0.8
        )

        self.wait(1)

        self.play(
            FadeOut(x_label),
            FadeOut(r_line),
            FadeOut(r_label),
            FadeOut(triangle[1]),
            FadeOut(triangle[2]),
            FadeOut(triangle[3]),
            run_time=0.65
        )

        triangle_fills = VGroup(triangle[0])

        # --------------------------------------------------
        # Add triangle areas
        # --------------------------------------------------

        for count, k in zip(
            range(2, 7),
            range(5)
        ):
            new_fill = make_triangle_fill(6, k)

            sum_string = "(" + "+".join(
                ["s"] * count
            ) + ")"

            new_formula = MathTex(
                r"A",
                r"=",
                r"\frac{1}{2}",
                r"r",
                sum_string,
                font_size=60
            )

            place_formula(new_formula)
            color_area(new_formula)
            new_formula[4].set_color(poly_color)

            triangle_fills.add(new_fill)

            self.play(
                FadeIn(new_fill),
                TransformMatchingTex(
                    formula,
                    new_formula
                ),
                run_time=0.6
            )

            formula = new_formula
            self.wait(0.18)

        # --------------------------------------------------
        # Six s's = 6s
        # Summation and spokes fade over 1 second
        # --------------------------------------------------

        sum_result = MathTex(
            r"=",
            r"\frac{1}{2}",
            r"r",
            r"(6s)",
            font_size=60
        )

        sum_result[3].set_color(poly_color)

        sum_result.next_to(
            formula,
            RIGHT,
            buff=0.22
        )

        self.play(
            Write(sum_result),
            FadeOut(spokes),
            run_time=1.0
        )

        self.wait(0.18)

        hexagon_formula = MathTex(
            r"A",
            r"_{\text{hexagon}}",
            r"=",
            r"\frac{1}{2}",
            r"r",
            r"(6s)",
            font_size=60
        )

        place_formula(
            hexagon_formula,
            0.5
        )

        color_area(hexagon_formula)
        hexagon_formula[5].set_color(poly_color)

        self.play(
            FadeOut(formula),
            FadeOut(sum_result),
            run_time=0.45
        )

        self.play(
            Write(hexagon_formula),
            run_time=1.4
        )

        self.wait(1.0)

        # --------------------------------------------------
        # n-gon formula and octagon appear together
        # --------------------------------------------------

        n_formula = MathTex(
            r"A",
            r"_{n\text{-gon}}",
            r"=",
            r"\frac{1}{2}",
            r"r",
            r"(",
            r"ns",
            r")",
            font_size=60
        )

        place_formula(n_formula)
        color_area(n_formula)
        n_formula[6].set_color(poly_color)

        self.add(polygon_fill)
        self.remove(*triangle_fills)

        n_sides_text = Text(
            "n equal sides",
            font_size=30,
            color=BLACK
        ).move_to(
            six_sides_text.get_center()
        )

        six_sides_text.become(n_sides_text)

        octagon_edge_length = np.linalg.norm(
            polygon_vertices(8)[1] -
            polygon_vertices(8)[0]
        )

        new_panel_edge = Line(
            LEFT * octagon_edge_length / 2,
            RIGHT * octagon_edge_length / 2,
            color=poly_color,
            stroke_width=polygon_edge.get_stroke_width()
        ).move_to(
            polygon_edge.get_center()
        )

        new_panel_s = MathTex(
            "s",
            font_size=60,
            color=poly_color
        ).next_to(
            new_panel_edge,
            UP,
            buff=0.1
        )

        octagon = make_polygon(8)
        octagon_fill = make_polygon_fill(8)

        self.play(
            ReplacementTransform(
                hexagon_formula,
                n_formula
            ),
            Transform(
                polygon,
                octagon
            ),
            Transform(
                polygon_fill,
                octagon_fill
            ),
            run_time=1.0
        )

        polygon_edge.become(new_panel_edge)
        edge_x.become(new_panel_s)

        self.play(
            FadeIn(side_panel, shift=UP * 0.1),
            run_time=0.55
        )

        self.wait(0.7)

        # --------------------------------------------------
        # Transform ns into perimeter
        # --------------------------------------------------

        perimeter_formula = MathTex(
            r"A",
            r"_{n\text{-gon}}",
            r"=",
            r"\frac{1}{2}",
            r"r",
            r"(",
            r"\text{perimeter}",
            r")",
            font_size=60
        )

        place_formula(perimeter_formula)
        color_area(perimeter_formula)
        perimeter_formula[6].set_color(poly_color)

        self.play(
            TransformMatchingTex(
                n_formula,
                perimeter_formula
            ),
            run_time=1.0
        )

        self.wait(0.9)

        # --------------------------------------------------
        # Increasing n with distinct polygon stages
        # The finite sequence leads into n tending to infinity.
        # --------------------------------------------------

        n_values = [
            9, 10, 11, 12, 14, 16,
            18, 22, 28, 40, 60, 99
        ]

        transition_times = [
            0.45, 0.45, 0.45, 0.45,
            0.40, 0.40, 0.38, 0.38,
            0.35, 0.35, 0.32, 0.30
        ]

        hold_times = [
            0.55, 0.55, 0.50, 0.50,
            0.45, 0.45, 0.40, 0.40,
            0.35, 0.35, 0.35, 0.55
        ]

        infinity_label = MathTex(
            r"n \longrightarrow \infty",
            font_size=42
        ).move_to(center_shift)
        n_label = MathTex("n", "=", "8", font_size=36).move_to(center_shift)
        self.play(FadeOut(side_panel), FadeIn(n_label), run_time=0.5)
        self.wait(0.65)

        for n, duration, hold in zip(
            n_values,
            transition_times,
            hold_times
        ):
            new_polygon = make_polygon(n)
            new_fill = make_polygon_fill(n)

            new_label = MathTex(
                "n", "=", str(n),
                font_size=36
            ).move_to(center_shift)

            animations = [
                Transform(
                    polygon,
                    new_polygon
                ),
                Transform(
                    polygon_fill,
                    new_fill
                )
            ]

            animations.append(TransformMatchingTex(n_label, new_label))

            self.play(
                *animations,
                run_time=duration,
                rate_func=smooth
            )

            n_label = new_label
            self.wait(hold)

        # --------------------------------------------------
        # Continue beyond the last displayed finite value.
        # The limit replaces n=99, then fades before the equations appear.
        # --------------------------------------------------

        infinity_label.move_to(center_shift)
        self.play(
            ReplacementTransform(n_label, infinity_label),
            run_time=0.8
        )
        self.wait(2.0)

        # --------------------------------------------------
        # Show the circle formula below the polygon formula.
        # Leave room for two vertical arrows between the corresponding terms.
        # --------------------------------------------------

        self.play(
            FadeOut(infinity_label),
            circle.animate.shift(UP * 0.9),
            polygon.animate.shift(UP * 0.9),
            polygon_fill.animate.shift(UP * 0.9),
            perimeter_formula.animate.move_to(
                LEFT * 0.8 + DOWN * 1.55
            ),
            run_time=0.6
        )

        circumference_formula = MathTex(
            r"A_{\mathrm{circ}}",
            r"=",
            r"\frac{1}{2}",
            r"r",
            r"(",
            r"\text{circumference}",
            r")",
            font_size=60
        ).move_to(LEFT * 0.8 + DOWN * 3.10)
        circumference_formula.set_color(BLACK)
        circumference_formula.shift(RIGHT * (
            perimeter_formula[2].get_center()[0]
            - circumference_formula[1].get_center()[0]
        ))

        area_term = VGroup(perimeter_formula[0], perimeter_formula[1])
        area_arrow = Arrow(
            area_term.get_bottom() + DOWN * 0.08,
            [area_term.get_center()[0], -2.58, 0],
            buff=0,
            color=BLACK,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.25
        )
        perimeter_term = perimeter_formula[6]
        perimeter_arrow = Arrow(
            perimeter_term.get_bottom() + DOWN * 0.08,
            [perimeter_term.get_center()[0], -2.58, 0],
            buff=0,
            color=BLACK,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.25
        )
        limit_arrows = VGroup(area_arrow, perimeter_arrow)
        self.play(Create(limit_arrows), run_time=0.6)
        self.wait(0.25)

        # Same vertex count and orientation as the
        # 99-gon, with vertices on the circle.
        limit_vertices = [
            np.array([
                r * math.cos((2*k + 1)*math.pi/99),
                r * math.sin((2*k + 1)*math.pi/99),
                0
            ])
            for k in range(99)
        ]

        limiting_polygon = Polygon(
            *limit_vertices,
            color=poly_color,
            fill_opacity=0
        ).shift(center_shift + UP * 0.9)

        limiting_fill = Polygon(
            *limit_vertices,
            stroke_width=0,
            fill_color=highlight_color,
            fill_opacity=0.18
        ).shift(center_shift + UP * 0.9)

        self.play(
            Transform(
                polygon,
                limiting_polygon
            ),
            Transform(
                polygon_fill,
                limiting_fill,
                run_time=2.0
            ),
            Write(circumference_formula, run_time=2.0),
            run_time=2.0,
            rate_func=smooth
        )

        # Remove the blue boundary.
        # Keep the disk blue through the circumference equation.
        self.play(
            FadeOut(polygon),
            circle.animate.set_stroke(
                color=BLACK,
                width=4
            ),
            run_time=0.4
        )

        self.wait(2.0)

        self.play(
            FadeOut(perimeter_formula),
            FadeOut(limit_arrows),
            polygon_fill.animate.set_fill(color=final_fill_color, opacity=0.50),
            run_time=0.5
        )

        # --------------------------------------------------
        self.play(
            circle.animate.shift(DOWN * 0.9),
            polygon_fill.animate.shift(DOWN * 0.9),
            circumference_formula.animate.set_color(BLACK).move_to(
                LEFT * 0.8 + DOWN * 2.55
            ),
            run_time=0.5
        )

        # Replace circumference with 2pi r
        # The disk is gray after the polygon equation and arrows disappear.
        # --------------------------------------------------

        circle_formula = MathTex(
            r"A",
            r"=",
            r"\frac{1}{2}",
            r"r",
            r"(2\pi r)",
            font_size=60
        )

        circle_formula[0].set_color(BLACK)
        final_extension = MathTex(
            r"=",
            r"\pi r^2",
            font_size=60
        ).next_to(circle_formula, RIGHT, buff=0.22)
        # Center the complete final expression before revealing its last term.
        VGroup(circle_formula, final_extension).move_to(
            LEFT * 0.8 + DOWN * 2.55
        )

        self.wait(0.9)
        self.play(
            TransformMatchingTex(circumference_formula, circle_formula),
            run_time=1.6
        )
        self.wait(0.3)

        self.play(
            Write(final_extension),
            run_time=1.0
        )

        self.wait(3)
